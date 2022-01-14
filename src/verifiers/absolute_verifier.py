# NOTE: Uses the KIHT value

from td_data_dict import TD_Data_Dictionary
from verifier_utils import find_matching_keys
from log import Logger

class AbsoluteVerifier():
    def __init__(self, template_file_path: str, verification_file_path: str, threshold: float):
        self.THRESHOLD = threshold
        self.template_file_path = template_file_path
        self.verification_file_path = verification_file_path
        self.template_td_data_dict = TD_Data_Dictionary(self.template_file_path)
        self.verification_td_data_dict = TD_Data_Dictionary(self.verification_file_path)
    
    def template_path(self):
        return self.template_file_path
    def verification_path(self):
        return self.verification_file_path
        
    def is_key_valid(self, key: str) -> bool:
        latencies = self.find_latency_averages(key)
        assert len(latencies) == 2
        if latencies[0] > latencies[1]:
            avg = latencies[0] / latencies[1]
            if avg in range(1, self.THRESHOLD):
                return True
            else: 
                return False
        elif latencies[0] < latencies[1]:
            avg = latencies[1] / latencies[0]
            if avg in range(1, self.THRESHOLD):
                return True
            else: 
                return False
        elif latencies[0] == latencies[1]:
            # If the two latnecies are equal than we know the quotient between them will always be 1 
            # and thus, always fall in the inclusive range of (1, THRESHOLD) so we can automatically
            # just return True
            return True

    def calculate_absolute_score(self):
        matches = find_matching_keys(self.template_file_path, self.verification_file_path)
        valids = self.find_all_valid_keys()
        return (1 - (len(valids) / len(matches)))

    def find_latency_averages(self, key: str):
        log = Logger()
        #NOTE: This function does not actually calculate the average latency 
        # for the key, rather it perform a lookup on the dictionary returned by calculate_key_hit_time() 
        # function for both of the td_data_dict's.
        # This is because the returned KHT dictionary already performs a mean operation if there are 
        # multiple latencies for a particular key
        template_hit_dict = self.template_td_data_dict.calculate_key_hit_time()
        verification_hit_dict = self.verification_td_data_dict.calculate_key_hit_time()
        key_matches = find_matching_keys(self.template_file_path, self.verification_file_path)
        if not key in key_matches:
            log.km_error("Key %s not found" % key)
            return
        t_latency = template_hit_dict.get(key)
        v_latency  = verification_hit_dict.get(key)
        return list(t_latency, v_latency)
    
    def find_all_valid_keys(self):
        valids = []
        matches = find_matching_keys(self.template_file_path, self.verification_file_path)
        for key in matches:
            if self.is_key_valid(key):
                valids.append(key)
        return valids