
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

}

exception ServerError {
    1: string reason,
}

exception RequestError {
    1: string reason,
}

service RegistService {
    void spider_register(1:string spiderid),
    void spider_unregister(1:string spiderid),
}

service SeedsService {
    /**
     * when spider is idle, it will request seeds from master
     * if the spider is not registed, master will auto do this for unregisted
     * spider
     * @TODO: spider should report its last time job info to master, include:
     * time, total page size, url num and so on 
     */
    SeedsPackage get_seeds(1:string spiderid),
    void add_seeds(1:SeedsPackage pkg),
    
    #latency
    i32 get_latency_time(1:string url),
}
