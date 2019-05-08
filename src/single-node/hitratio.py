from mcav.sca import SCA
from mcav.zipf import Zipf
from mcav.scav import SCAV

if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 40
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents

    sca_validation = SCAV(
        content_amount, cache_size, p_dict, request_rate, staleness_time)
    sca = SCA(content_amount, cache_size, p_dict)
    print(sca.totalHitRatio())
    print (sca_validation.totalHitRatio())
