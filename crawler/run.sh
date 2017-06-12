#!/usr/bin/env bash
where_am_i=$(dirname $(realpath -s $0))
${scrapy:-scrapy} crawl meizitu --logfile $where_am_i/`date +'%Y_%m_%d_%H_%M_%S'`.log


