from mcav.zipf import Zipf
from mcav.sca import SCA
from mcav.scav import SCAV
from mcav.mca import MCA
from mcav.mcav import MCAV


if __name__ == "__main__":
    content_amount = 1000
    cache_size = 100
    request_rate = 10.0
    staleness_time = 60
    z = 0.8  # zipf parameter
    zipf = Zipf(content_amount, z)
    p_dict = zipf.popularity()  # popularity of the contents
    # print (p_dict)

    sca = SCA(content_amount, cache_size, p_dict)
    print(sca.totalHitRatio())
    
    scav = SCAV(content_amount, cache_size, p_dict, request_rate, staleness_time)
    print(scav.totalHitRatio())

    mca = MCA(content_amount, cache_size, p_dict, request_rate)
    print(mca.totalHitRatio())

    mcav = MCAV(content_amount, cache_size, p_dict, request_rate, staleness_time)
    print(mcav.totalHitRatio())