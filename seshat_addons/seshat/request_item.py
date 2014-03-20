#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
Main framework app

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2014
http://joshashby.com
joshuaashby@joshashby.com
"""
import seshat.request as request
import logging
logger = logging.getLogger("seshat.request")

import models.redis.session.sessionModel as sm
import models.redis.bucket.bucketModel as bm
import models.redis.announcement.announcementModel as am


class RequestItem(request.BaseRequest):
    cookie_name = "bug_sid"

    def build_session(self):
        self.session = sm.session("session:"+self.session_ID)

    def build_cfg(self):
        self.buckets = bm.CfgBuckets()
        self.announcements = am.CfgAnnouncements()

        self.has_announcements = (len(self.announcements._data)>=1)
