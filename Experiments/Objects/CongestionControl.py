from abc import ABC, abstractmethod
from typing import Optional
from Enums.BBRStage import BBRStage
import random
import math

class CongestionControl(ABC):
    """Abstract base class for congestion control algorithms."""
    
    def __init__(self):
        self.cwnd: float = 1.0
        self.ssthresh: float = 64
        self.rto: int = 1000
        self.last_ack_tick: int = 0
        self.dup_ack_count: int = 0
        self.in_fast_recovery: bool = False
        self.recovery_seq: int = 0
    
    @abstractmethod
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Called when a packet is sent from the host.

        Args:
            seq_num (int): The seq number of the packet
            current_tick (int): The tick in the simulation
        """
        pass
    
    @abstractmethod
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when an ACK is received.

        Args:
            ack_num (int): The ACK number
            current_tick (int): The tick in the simulation

        Returns:
            Optional[float]: The new CWND of the host
        """
        pass
    
    @abstractmethod
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a packet times out.

        Args:
            seq_num (int): The seq number of the timed out packet
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND of the host after a timeout
        """
        pass
    
    @abstractmethod
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when a dup ACK occurs.

        Args:
            ack_num (int): The ACK number of the dup ACK
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND of the host after a dup ACK
        """
        pass
    
    def get_cwnd(self) -> float:
        """Gets the current CWND.

        Returns:
            float: The current CWND of the CC algorithm
        """
        return self.cwnd
    
    def get_ssthresh(self) -> float:
        """Gets the slow start threshold.

        Returns:
            float: The slow start threshold of the cc algorithm
        """
        return self.ssthresh
    
    def get_rto(self) -> int:
        """Gets the retransmission timeout time.

        Returns:
            int: The retransmission timeout time
        """
        return self.rto


class RenoCongestionControl(CongestionControl):
    """Reno congestion control algorithm implementation."""
    
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """No events on packet sent.

        Args:
            seq_num (int): The seq number of the sent packet
            current_tick (int): The current tick in the simulation
        """
        pass
    
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handles a host getting an ACK for Reno.

        Args:
            ack_num (int): The ACK number.
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND after an ACK is received
        """
        self.last_ack_tick = current_tick
        
        if self.in_fast_recovery:
            if ack_num >= self.recovery_seq:
                self.in_fast_recovery = False
                self.dup_ack_count = 0
                self.cwnd = self.ssthresh
        else:
            if self.cwnd < self.ssthresh:
                self.cwnd += 1
            else:
                self.cwnd += 1.0 / self.cwnd
        
        return self.cwnd
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a packet times out in Reno.

        Args:
            seq_num (int): The sequence number of the timed out packet
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND after a packet times out
        """
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1
        self.in_fast_recovery = False
        self.dup_ack_count = 0
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Handles on a duplicate ACK/retransmission

        Args:
            ack_num (int): The ACK number received
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND after the duplicate ACK
        """
        self.dup_ack_count += 1
        if self.dup_ack_count == 3 and not self.in_fast_recovery:
            # Fast retransmit
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = self.ssthresh + 3
            self.in_fast_recovery = True
            self.recovery_seq = ack_num + 1
            return self.cwnd
        return None
    
class VegasCongestionControl(CongestionControl):
    """TCP Vegas congestion control algorithm implementation."""
    
    def __init__(self):
        super().__init__()
        self.base_rtt: float = float('inf')
        self.current_rtt: float = float('inf')
        self.alpha: float = 1.0
        self.beta: float = 3.0
        self.packet_sent_times: dict[int, int] = {}
        
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Called when a packet is sent.

        Args:
            seq_num (int): The sequence number of the sent packet
            current_tick (int): The current tick of the simulation
        """
        self.packet_sent_times[seq_num] = current_tick
        
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when an ACK is received.

        Args:
            ack_num (int): The received ACK number
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND
        """
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
                self.cwnd = max(self.cwnd - 1, 1)
            # Else: keep cwnd unchanged (between alpha and beta)
        
        return self.cwnd
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a packet times out.

        Args:
            seq_num (int): The sequence number of the packet that timed out
            current_tick (int): The current tick in the simulation

        Returns:
            Optional[float]: The new CWND
        """
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
        """Called when a duplicate ACK is received.

        Args:
            ack_num (int): The ACK number of the duplicate ACK
            current_tick (int): The current tick of the simulation

        Returns:
            Optional[float]: The new CWND after a duplicate ACK event
        """
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


class BBRCongestionControl(CongestionControl):
    """BBR congestion control."""
    
    def __init__(self):
        super().__init__()
        self.btl_bw = 0.0
        self.rt_prop = float('inf')
        self.min_rtt = float('inf')
        self.delivery_rate = 0.0
        self.pacing_gain = 2.89
        self.cwnd_gain = 2.0 
        self.state = BBRStage.STARTUP
        self.cycle_index = 0
        self.rt_prop_stamp = 0
        self.packet_count = 0
        self.ack_count = 0
        
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Called on a packet sent for BBR algorithm.

        Args:
            seq_num (int): The sequence number of the sent packet
            current_tick (int): The current tick in the simulation
        """
        self.packet_count += 1
        if self.rt_prop_stamp == 0:
            self.rt_prop_stamp = current_tick
        
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when an ACK is received.

        Args:
            ack_num (int): The ACK number received
            current_tick (int): The current tick of the simulation

        Returns:
            Optional[float]: The new CWND after the ACK is received
        """
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
        """Updates the state of the state of the BBR state machine.

        Args:
            current_tick (int): The current tick of the simulation
        """
        if self.state == BBRStage.STARTUP:
            if self.btl_bw > 0 and self.cwnd >= 2 * self.btl_bw * self.rt_prop:
                self.state = BBRStage.DRAIN
                self.pacing_gain = 1.0 / 2.89  # Inverse of startup gain
        elif self.state == BBRStage.DRAIN:
            if self.cwnd <= self.btl_bw * self.rt_prop:
                self.state = BBRStage.PROB_BW
                self.pacing_gain = 1.0
                self.cycle_index = 0
        elif self.state == BBRStage.PROB_BW:
            # Cycle through gains: 1.25, 0.75, 1, 1, 1, 1, 1, 1
            gains = [1.25, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
            self.pacing_gain = gains[self.cycle_index % len(gains)]
            self.cycle_index += 1
            
            # Check for PROBE_RTT every 10 seconds (simplified)
            if current_tick % 10000 == 0:
                self.state = BBRStage.PROB_RTT
        elif self.state == BBRStage.PROB_RTT:
            if current_tick - self.last_ack_tick > self.rt_prop:
                self.state = BBRStage.PROB_BW
                self.cycle_index = 0
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a timeout occurs for a packet.

        Args:
            seq_num (int): The sequence number of the timed out packet
            current_tick (int): The current tick of the simulation

        Returns:
            Optional[float]: The new CWND after a timeout
        """
        # BBR doesn't reduce cwnd on timeout like Reno
        # Instead, it updates estimates
        self.btl_bw *= 0.9
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called on a duplicate ACK.

        Args:
            ack_num (int): The ACK number of the duplicate ACK
            current_tick (int): The current tick of the simulation

        Returns:
            Optional[float]: The new CWND
        """
        return None


class RLCongestionControl(CongestionControl):
    """Reinforcement Learning-based congestion control algorithm."""
    
    def __init__(self):
        super().__init__()
        # RL parameters
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1  # Exploration rate
        
        # State variables
        self.current_state = "slow_start"
        self.last_rtt = float('inf')
        self.rtt_samples = []
        self.packet_loss_count = 0
        self.successful_transmissions = 0
        
        # Action space: 0=decrease, 1=maintain, 2=increase
        self.actions = [0, 1, 2]
        
        # Simple Q-table: state -> action -> value
        self.q_table = {
            "slow_start": {0: 0, 1: 0, 2: 1},  # Prefer increase in slow start
            "congestion_avoidance": {0: 0, 1: 1, 2: 0.5},  # Prefer maintain in congestion avoidance
            "congestion_detected": {0: 1, 1: 0.5, 2: 0},  # Prefer decrease when congestion detected
            "recovery": {0: 0.5, 1: 1, 2: 0}  # Prefer maintain in recovery
        }
        
        # State tracking
        self.last_action = None
        self.last_state = None
        self.last_reward = 0
        
    def _get_state(self, current_tick: int) -> str:
        """Determine the current state based on network conditions.
        
        Args:
            current_tick (int): Current simulation tick
            
        Returns:
            str: Current state identifier
        """
        # Calculate average RTT if we have samples
        avg_rtt = float('inf')
        if self.rtt_samples:
            avg_rtt = sum(self.rtt_samples) / len(self.rtt_samples)
        
        # State determination logic
        if self.cwnd < self.ssthresh:
            return "slow_start"
        elif self.packet_loss_count > 0:
            return "congestion_detected"
        elif self.in_fast_recovery:
            return "recovery"
        else:
            return "congestion_avoidance"
    
    def _choose_action(self, state: str) -> int:
        """Choose an action using epsilon-greedy policy.
        
        Args:
            state (str): Current state
            
        Returns:
            int: Chosen action (0=decrease, 1=maintain, 2=increase)
        """
        if random.random() < self.epsilon:
            # Explore: random action
            return random.choice(self.actions)
        else:
            # Exploit: best known action
            action_values = self.q_table[state]
            return max(action_values, key=action_values.get)
    
    def _update_q_value(self, state: str, action: int, reward: float, next_state: str):
        """Update Q-value using Q-learning update rule.
        
        Args:
            state (str): Previous state
            action (int): Action taken
            reward (float): Reward received
            next_state (str): New state after action
        """
        current_q = self.q_table[state][action]
        max_next_q = max(self.q_table[next_state].values())
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def _calculate_reward(self, rtt: float, packet_loss: bool, throughput: float = 0.0) -> float:
        """Calculate reward based on network performance.
        
        Args:
            rtt (float): Current RTT measurement
            packet_loss (bool): Whether packet loss occurred
            throughput (float): Current throughput in bps
            
        Returns:
            float: Calculated reward
        """
        reward = 0
        
        # Reward for high throughput (primary objective)
        if throughput > 0:
            # Normalize throughput reward (higher throughput = higher reward)
            # Assuming typical throughput range 0-10000 bps, scale to 0-50 reward
            reward += (throughput / 200.0)
        
        # Reward for low RTT (secondary objective)
        if rtt < float('inf'):
            reward += 20.0 / (1.0 + rtt/50.0)  # Higher reward for lower RTT
        
        # Penalty for packet loss (strong negative signal)
        if packet_loss:
            reward -= 30.0
        
        # Reward for efficient window size (tertiary objective)
        if 15 <= self.cwnd <= 80:
            reward += 3.0  # Optimal window size range
        elif self.cwnd < 5:
            reward -= 1.0  # Too conservative
        elif self.cwnd > 150:
            reward -= 2.0  # Too aggressive
            
        return reward
    
    def _apply_action(self, action: int):
        """Apply the chosen action to adjust congestion window.
        
        Args:
            action (int): Action to apply (0=decrease, 1=maintain, 2=increase)
        """
        if action == 0:  # Decrease
            self.cwnd = max(self.cwnd * 0.7, 1.0)
        elif action == 2:  # Increase
            if self.cwnd < self.ssthresh:
                self.cwnd += 1  # Slow start
            else:
                self.cwnd += 1.0 / self.cwnd  # Congestion avoidance
    
    def on_packet_sent(self, seq_num: int, current_tick: int):
        """Called when a packet is sent.
        
        Args:
            seq_num (int): Sequence number of sent packet
            current_tick (int): Current simulation tick
        """
        # Store sent time for RTT calculation
        if not hasattr(self, 'packet_sent_times'):
            self.packet_sent_times = {}
        self.packet_sent_times[seq_num] = current_tick
    
    def on_ack_received(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when an ACK is received.
        
        Args:
            ack_num (int): ACK number received
            current_tick (int): Current simulation tick
            
        Returns:
            Optional[float]: New congestion window
        """
        self.last_ack_tick = current_tick
        self.successful_transmissions += 1
        
        # Calculate RTT if we have the sent time
        rtt = float('inf')
        if hasattr(self, 'packet_sent_times') and ack_num in self.packet_sent_times:
            sent_time = self.packet_sent_times[ack_num]
            rtt = current_tick - sent_time
            self.rtt_samples.append(rtt)
            # Keep only recent samples
            if len(self.rtt_samples) > 10:
                self.rtt_samples.pop(0)
            del self.packet_sent_times[ack_num]
        
        # Get current state
        current_state = self._get_state(current_tick)
        
        # Choose and apply action
        action = self._choose_action(current_state)
        self._apply_action(action)
        
        # Get current throughput (simplified estimation based on window size and RTT)
        estimated_throughput = 0.0
        if rtt > 0 and rtt < float('inf'):
            estimated_throughput = (self.cwnd * 8) / (rtt / 1000.0)  # Convert to bps
        
        # Calculate reward including throughput
        reward = self._calculate_reward(rtt, False, estimated_throughput)
        
        # Update Q-table if we have previous state and action
        if self.last_state is not None and self.last_action is not None:
            self._update_q_value(self.last_state, self.last_action, self.last_reward, current_state)
        
        # Store current state and action for next update
        self.last_state = current_state
        self.last_action = action
        self.last_reward = reward
        
        return self.cwnd
    
    def on_timeout(self, seq_num: int, current_tick: int) -> Optional[float]:
        """Called when a packet times out.
        
        Args:
            seq_num (int): Sequence number of timed out packet
            current_tick (int): Current simulation tick
            
        Returns:
            Optional[float]: New congestion window
        """
        self.packet_loss_count += 1
        
        # Get current state
        current_state = self._get_state(current_tick)
        
        # Choose action (more likely to decrease on timeout)
        action = 0  # Always decrease on timeout
        
        # Apply aggressive reduction
        self.ssthresh = max(self.cwnd / 2, 2)
        self.cwnd = 1.0
        self.in_fast_recovery = False
        self.dup_ack_count = 0
        
        # Calculate reward (penalize timeout heavily)
        reward = self._calculate_reward(float('inf'), True)
        
        # Update Q-table
        if self.last_state is not None and self.last_action is not None:
            self._update_q_value(self.last_state, self.last_action, self.last_reward, current_state)
        
        # Reset tracking
        self.last_state = None
        self.last_action = None
        
        return self.cwnd
    
    def on_dup_ack(self, ack_num: int, current_tick: int) -> Optional[float]:
        """Called when a duplicate ACK is received.
        
        Args:
            ack_num (int): ACK number of duplicate ACK
            current_tick (int): Current simulation tick
            
        Returns:
            Optional[float]: New congestion window
        """
        self.dup_ack_count += 1
        self.packet_loss_count += 1
        
        if self.dup_ack_count == 3 and not self.in_fast_recovery:
            # Fast retransmit
            self.ssthresh = max(self.cwnd / 2, 2)
            self.cwnd = self.ssthresh
            self.in_fast_recovery = True
            self.recovery_seq = ack_num + 1
            
            # Get current state and calculate reward
            current_state = self._get_state(current_tick)
            reward = self._calculate_reward(float('inf'), True)
            
            # Update Q-table
            if self.last_state is not None and self.last_action is not None:
                self._update_q_value(self.last_state, self.last_action, self.last_reward, current_state)
            
            self.last_state = None
            self.last_action = None
            
            return self.cwnd
        
        return None
