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

import models.rethink.request.requestModel as rm


class RequestItem(request.BaseRequest):
    cookie_name = "bug_sid"

    def build_session(self):
        self.session = sm.session("session:"+self.session_ID)

    def build_cfg(self):
        self.buckets = bm.CfgBuckets()
        self.announcements = am.CfgAnnouncements()

        self.has_announcements = (len(self.announcements._data)>=1)

    def log(self, head):
        if head.error is not None or "404" in head.status:
            error = head.error[1] if head.error is not None else ""
            rm.Request.new_request(user=self.session.id,
                                   ip=self.remote,
                                   agent=self.user_agent,
                                   url=self._raw_url,
                                   method=self.method,
                                   referer=self.referer,
                                   status=head.status,
                                   error=error)
