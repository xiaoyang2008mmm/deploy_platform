# -*- coding: utf-8 -*- 
import functools,tornado
def isadmin(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        else:
            if self.current_user !="admin":
		raise tornado.web.HTTPError(403)
                #self.write("您没有权限,页面即将跳转 ")
                return
        return method(self, *args, **kwargs)
    return wrapper
