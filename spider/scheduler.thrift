struct Seed {
    1: string url,
    2: string content_group,
    3: string pl_group, 
    4: i32 max_idepth = 0,
    5: i32 max_xdepth = 0,
    6: i32 cur_idepth = 0,
    7: i32 cur_xdepth = 0,
    8: i32 priority,
    9: i32 crawl_interval = 10,
    10: i32 seed_frequency = 0,
}

struct SeedsPackage {
    1: string ID,
    2: list<Seed> seeds = [],
}

struct JobReport {
    /*seconds*/
    1: string spiderid,
    2: i32 work_time = 0,
    3: i32 idle_time = 0,
    4: i32 fail_url_num = 0,
    5: i32 crawled_url_num = 0,
    6: i32 crawled_page_size = 0,
}

exception ServerError {
    1: string reason = 'unkown server internal error',
}

exception RequestError {
    1: string reason = 'illeage request',
}

service Scheduler {

    void ping()

    void do_register(1: string spiderid),

    void do_unregister(1: string spiderid),

    /**
     * if the spider is unregisted, 
     *      master will do auto registration
     * spider reports its last job info to master
     */
    SeedsPackage get_seeds(1: string spiderid, 3: JobReport report) throws (1:ServerError err),
    
    /*
     */
    void add_seeds(1: string clientid, 2: SeedsPackage pkg) throws (1:ServerError err), 
    
    /*
     */
    i32 get_latency_time(1: string spiderid, 2: string url),
}
