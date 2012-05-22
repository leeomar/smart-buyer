struct Seed {
    1: string url,
    2: string content_group,
    3: i32 max_idepth,
    4: i32 max_xdepth,
    5: i32 cur_idepth,
    6: i32 cur_xdepth,
    7: i32 priority,
    8: string pl_group, 
}

struct SeedsPackage {
    1: string ID,
    2: required list<Seed> seeds,
}

struct JobReport {
    /*seconds*/
    1:i32 work_time = 0,
    2:i32 idle_time = 0,
    4:i32 fail_url_num = 0,
    3:i32 crawled_url_num = 0,
    5:i32 crawled_page_size = 0,
}

exception ServerError {
    1: string reason = 'unkown server internal error',
}

exception RequestError {
    1: string reason = 'illeage request',
}

service RegistService {
    void spider_register(1:string spiderid),
    void spider_unregister(1:string spiderid),
}

service SeedsService {
    /**
     * if the spider is unregisted, 
     *      master will do auto registration
     * spider reports its last job info to master
     */
    SeedsPackage get_seeds(1:string spiderid, 3:JobReport report),

    /*
     */
    void add_seeds(1:SeedsPackage pkg, 2:string spiderid), 
    
    /*
     */
    i32 get_latency_time(1:string url, 2:string spiderid),
}
