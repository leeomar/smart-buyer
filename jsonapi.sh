#/bin/sh

SCRAPYD_URL='http://localhost:6801'

help()
{
    echo "Usage:"
    echo "  sh jsonapi.sh <command> [args]"
    echo ""
    echo "Available commands:"
    echo "  schedule: project spider"
    echo "  cancel: project job "
    echo "  addversion: project version egg "
    echo "  delversion: project version"
    echo "  delproject: project"
    echo "  listversions: project"
    echo "  listspiders: project"
    echo "  listjobs: project"
    echo "  listprojects "
}

assertparam()
{
    actual=$1
    expect=$2
    if [ $actual -lt $expect ]; then
        echo "Error: expect $2 args"
        help
        exit
    fi
}

addversion()
{
    assertparam $# 4
    project=$2
    version=$3
    egg=$4
    curl $SCRAPYD_URL/addversion.json -F project=$project -F version=$version -F egg=$egg
}

delversion()
{
    assertparam $# 3
    project=$2
    version=$3
    curl $SCRAPYD_URL/delversion.json -d project=$project -d version=$version
}

schedule()
{
    assertparam $# 3
    project=$2
    spider=$3
    echo "schedule project=$project, spider=$spider"
    curl $SCRAPYD_URL/schedule.json -d project=$project -d spider=$spider -d jobid=$spider
}

cancel()
{
    assertparam $# 3
    project=$2
    job=$3
    curl $SCRAPYD_URL/cancel.json -d project=$project -d job=$job
}

listprojects()
{
    curl $SCRAPYD_URL/listprojects.json
}

listversions()
{
    assertparam $# 2
    project=$2    
    curl $SCRAPYD_URL/listversions.json?project=$project
}

listspiders()
{
    assertparam $# 2
    project=$2    
    curl $SCRAPYD_URL/listspiders.json?project=$project
}

listjobs()
{
    assertparam $# 2
    project=$2    
    curl $SCRAPYD_URL/listjobs.json?project=$project
}

delproject()
{
    assertparam $# 2
    project=$2    
    curl $SCRAPYD_URL/delproject.json -d project=$project
}

main()
{
    assertparam $# 1
    case $1 in
        schedule)
            schedule $@
        ;;
        cancel)
            cancel $@
        ;;
        delproject)
            delproject $@
        ;;
        addversion)
            addversion $@
        ;;
        delversion)
            delversion $@
        ;;
        listversions)
            listversions $@
        ;;
        listspiders)
            listspiders $@
        ;;
        listjobs)
            listjobs $@
        ;;
        listprojects)
            listprojects $@
        ;;
        help)
            help
        ;;
        *)
            echo "Error: unkown command"
            help
        ;;
    esac
}
main $@ 
