from abc import ABC, abstractmethod
from typing import Optional

class CongestionControl(ABC):
    """Abstract base class for congestion control algorithms."""
    
    def __init__(self):
        self.cwnd: float = 1.0
        self.ssthresh: float = 64.0
        self.rto: int = 1000
        self.last_ack_tick: int = 0
        self.dup_ack_count: int = 0
        self.in_fast_recovery: bool = False
        self.recovery_seq: int = 0
    
    @abstractmethod
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Called when a packet is sent."""
        pass
    
    @abstractmethod
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when an ACK is received. Returns new cwnd value."""
        pass
    
    @abstractmethod
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a packet times out. Returns new cwnd value."""
        pass
    
    @abstractmethod
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when a duplicate ACK is received. Returns new cwnd value."""
        pass
    
    def get_cwnd(self) -> float:
        """Get current congestion window size."""
        return self.cwnd
    
    def get_ssthresh(self) -> float:
        """Get current slow start threshold."""
        return self.ssthresh
    
    def get_rto(self) -> int:
        """Get current retransmission timeout."""
        return self.rto


class RenoCongestionControl(CongestionControl):
    """Reno congestion control algorithm implementation."""
    
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """No specific action on packet sent for Reno."""
        pass
    
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle ACK reception for Reno."""
        self.last_ack_tick = current_tick
        
        if self.in_fast_recovery:
            if ack_num >= self.recovery_seq:
                self.in_fast_recovery = False
                self.dup_ack_count = 0
                self.cwnd = self.ssthresh
        else:
            # Slow start or congestion avoidance
            if self.cwnd < self.ssthresh:
                self.cwnd += 1  # Slow start: exponential growth
            else:
                self.cwnd += 1.0 / self.cwnd  # Congestion avoidance: additive increase
        
        return self.cwnd
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Handle timeout for Reno."""
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1
        self.in_fast_recovery = False
        self.dup_ack_count = 0
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle duplicate ACK for Reno fast retransmit."""
        self.dup_ack_count += 1
        if self.dup_ack_count == 3 and not self.in_fast_recovery:
            # Fast retransmit
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = self.ssthresh + 3
            self.in_fast_recovery = True
            self.recovery_seq = ack_num + 1
            return self.cwnd
        return None


class BBRCongestionControl(CongestionControl):
    """BBR (Bottleneck Bandwidth and Round-trip propagation time) congestion control."""
    
    def __init__(self):
        super().__init__()
        self.btl_bw = 0.0
        self.rt_prop = float('inf')
        self.min_rtt = float('inf')
        self.delivery_rate = 0.0
        self.pacing_gain = 2.89
        self.cwnd_gain = 2.0 
        self.state = "STARTUP"
        self.cycle_index = 0
        self.rt_prop_stamp = 0
        self.packet_count = 0
        self.ack_count = 0
        
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Record packet sent for BBR timing."""
        self.packet_count += 1
        if self.rt_prop_stamp == 0:
            self.rt_prop_stamp = current_tick
        
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle ACK reception for BBR."""
        self.last_ack_tick = current_tick
        self.ack_count += 1
        
        # Calculate RTT sample (simplified)
        rtt_sample = current_tick - self.rt_prop_stamp
        if rtt_sample < self.min_rtt:
            self.min_rtt = rtt_sample
            self.rt_prop = self.min_rtt
        
        # Estimate delivery rate (simplified)
        if self.packet_count > 0 and self.ack_count > 0:
            self.delivery_rate = self.ack_count / (current_tick - self.rt_prop_stamp)
            if self.delivery_rate > self.btl_bw:
                self.btl_bw = self.delivery_rate
        
        # Update state machine
        self._update_state(current_tick)
        
        # Calculate new cwnd based on BBR formula
        self.cwnd = self.btl_bw * self.rt_prop * self.cwnd_gain
        self.cwnd = max(self.cwnd, 1)  # Ensure at least 1
        
        # Reset counters for next round
        if self.ack_count >= self.packet_count:
            self.packet_count = 0
            self.ack_count = 0
            self.rt_prop_stamp = current_tick
        
        return self.cwnd
    
    def _update_state(self, current_tick: int):
        """Update BBR state machine."""
        if self.state == "STARTUP":
            if self.btl_bw > 0 and self.cwnd >= 2 * self.btl_bw * self.rt_prop:
                self.state = "DRAIN"
                self.pacing_gain = 1.0 / 2.89  # Inverse of startup gain
        elif self.state == "DRAIN":
            if self.cwnd <= self.btl_bw * self.rt_prop:
                self.state = "PROBE_BW"
                self.pacing_gain = 1.0
                self.cycle_index = 0
        elif self.state == "PROBE_BW":
            # Cycle through gains: 1.25, 0.75, 1, 1, 1, 1, 1, 1
            gains = [1.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            self.pacing_gain = gains[self.cycle_index % len(gains)]
            self.cycle_index += 1
            
            # Check for PROBE_RTT every 10 seconds (simplified)
            if current_tick % 10000 == 0:
                self.state = "PROBE_RTT"
        elif self.state == "PROBE_RTT":
            if current_tick - self.last_ack_tick > self.rt_prop:
                self.state = "PROBE_BW"
                self.cycle_index = 0
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Handle timeout for BBR."""
        # BBR doesn't reduce cwnd on timeout like Reno
        # Instead, it updates estimates
        self.btl_bw *= 0.9  # Reduce bandwidth estimate slightly
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle duplicate ACK for BBR."""
        # BBR doesn't use fast retransmit in the same way as Reno
        # Just update estimates if needed
        return None
class VegasCongestionControl(CongestionControl):
    """TCP Vegas congestion control algorithm implementation."""
    
    def __init__(self):
        super().__init__()
        self.base_rtt: float = float('inf')  # Minimum observed RTT
        self.current_rtt: float = float('inf')  # Current RTT sample
        self.alpha: float = 1.0  # Vegas parameter for lower threshold
        self.beta: float = 3.0   # Vegas parameter for upper threshold
        self.packet_sent_times: dict[int, int] = {}  # Track when packets were sent
        
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Record packet sent time for RTT calculation."""
        self.packet_sent_times[seq_num] = current_tick
        
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle ACK reception for Vegas."""
        self.last_ack_tick = current_tick
        
        # Calculate RTT if we have the sent time for this packet
        if ack_num in self.packet_sent_times:
            sent_time = self.packet_sent_times[ack_num]
            self.current_rtt = current_tick - sent_time
            
            # Update base RTT (minimum observed RTT)
            if self.current_rtt < self.base_rtt:
                self.base_rtt = self.current_rtt
            
            # Remove the recorded sent time
            del self.packet_sent_times[ack_num]
        
        # Calculate expected and actual throughput using base RTT and current RTT
        if self.base_rtt != float('inf') and self.current_rtt != float('inf'):
            expected_throughput = self.cwnd / self.base_rtt
            actual_throughput = self.cwnd / self.current_rtt
            
            # Calculate the difference (number of extra packets due to congestion)
            diff = (expected_throughput - actual_throughput) * self.base_rtt
            
            # Adjust congestion window based on Vegas algorithm
            if diff < self.alpha:
                # Below lower threshold: increase cwnd
                self.cwnd += 1
            elif diff > self.beta:
                # Above upper threshold: decrease cwnd
                self.cwnd = max(self.cwnd - 1, 1)  # Ensure cwnd doesn't go below 1
            # Else: keep cwnd unchanged (between alpha and beta)
        
        return self.cwnd
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Handle timeout for Vegas."""
        # Vegas responds to timeouts by reducing cwnd more aggressively
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1
        self.in_fast_recovery = False
        self.dup_ack_count = 0
        
        # Reset RTT measurements on timeout
        self.base_rtt = float('inf')
        self.current_rtt = float('inf')
        
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handle duplicate ACK for Vegas."""
        # Vegas doesn't use fast retransmit in the same way as Reno
        # But we can still respond to duplicate ACKs
        self.dup_ack_count += 1
        if self.dup_ack_count == 3 and not self.in_fast_recovery:
            # Similar to Reno's fast retransmit but with Vegas adjustments
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = self.ssthresh
            self.in_fast_recovery = True
            self.recovery_seq = ack_num + 1
            return self.cwnd
        return None
