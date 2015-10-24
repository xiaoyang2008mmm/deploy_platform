# -*- coding: utf-8 -*- 
import sys,os,subprocess
reload(sys)
sys.setdefaultencoding('utf8')

import bcrypt
from auth import isadmin
import shutil
import tornado.web
import time , thread
from modules.ansible_mod import *
from modules.shell_timeout import *
from mail import Mail
class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
       return self.application.db
    def get_current_user(self):
       return self.get_secure_cookie("user")

class ChartHandler(BaseHandler):
    def get(self):
        self.render('chart.html') 

class Develop_Handler(BaseHandler):
    def get(self):
        self.render('develop.html') 
class Base_Handler(BaseHandler):
    '''
    base.html获取当前用户
    '''
    def get(self):
	current_user=self.current_user
	self.render("base.html",current_user=current_user)

class User_Group_Handler(BaseHandler):
    """
    用户分组页面
    """
    def get(self):
	u_group_info = self.db.lrange("user_group",0,-1)
	u_hash_info = self.db.hgetall("usergroup_hash")
        _dict = { "u_group_info" : u_group_info ,'u_hash_info':u_hash_info }
        self.render('user_group.html' ,**_dict)

class Role_Handler(BaseHandler):
    '''
    角色页面
    '''
    def get(self):
	u_role_info = self.db.lrange("user_role",0,-1)
	u_hash_info = self.db.hgetall("userrole_hash")
        _dict = { "u_role_info" : u_role_info ,'u_hash_info':u_hash_info}
        self.render('role.html' ,**_dict )

class User_Handler(BaseHandler):
    '''
    用户信息页面
    '''
    def get(self):
	u_group_info = self.db.lrange("user_group",0,-1)
        u_role_info = self.db.lrange("user_role",0,-1)
	user_info = self.db.hgetall("useradd_hash")
	_dict = { "u_group_info" : u_group_info ,"u_role_info" : u_role_info ,"user_info" : user_info}
        self.render('user.html' ,**_dict )

class History_Handler(BaseHandler):
    '''
    发布历史记录页面 
    '''
    @isadmin
    def get(self):
	history_info = self.db.hgetall("history_hash")
	_dict = {"history_info" : history_info}
        self.render('history.html',**_dict) 

class Ssh_Page_Handler(BaseHandler):
    '''
    ssh服务器设置页面
    '''
    def get(self):
        self.render('ssh_page.html') 

class System_Handler(BaseHandler):
    '''
    系统设置页面
    '''
    def get(self):
        self.render('system.html') 

class View_Handler(BaseHandler):
    ''' 
    设置具体job的信息
    ''' 
    def get(self):
	data = self.db.lrange("PROJECT_NAME",0,-1)
	host_list = get_host_list(pattern="all")
        self.render('view.html', data = data, host_list = host_list) 

class All_Handler(BaseHandler):
    '''
    在首页展示分组的汇总信息
    '''
    @tornado.web.authenticated
    def get(self,group_name):
        self.group_name = group_name 
	data = self.db.lrange("PROJECT_NAME",0,-1)
	group_table = self.db.hgetall(self.group_name)
        self.render('index.html', data = data, group_table = group_table ) 
class Index_Handler(BaseHandler):
    '''
    重定向到all汇总信息页面
    '''
    @tornado.web.authenticated
    def get(self):
	data = self.db.lrange("PROJECT_NAME",0,-1)
        group_hash_key = ''.join((eval(data[0])).keys())
	self.redirect('/all/%s/'%(group_hash_key) , permanent=True)

class Post_View_Handler(BaseHandler):
    '''
    提交新项目或者修改项目
    '''
    def post(self):
        pro_name 	= self.get_argument("pro_name")
        pro_desc 	= self.get_argument("pro_desc")
        git_addr 	= self.get_argument("git_addr")
        exec_shell_1 	= (self.get_argument("exec_shell_1").encode("utf-8")).split("\n")
        exec_shell_2 	= (self.get_argument("exec_shell_2").encode("utf-8")).split("\n")
        ssh_server 	= self.get_argument("ssh_server")
        local_path 	= self.get_argument("local_path")
        remove_path 	= self.get_argument("remove_path")
        remote_path 	= self.get_argument("remote_path")
        mail_name 	= self.get_argument("mail_name")
        mail_subject 	= self.get_argument("mail_subject")
        mail_data 	=  (self.get_argument("mail_data").encode("utf-8")).split("\n")
        select_group	= self.get_argument("select_group")
        remote_exec_shell =  (self.get_argument("remote_exec_shell").encode("utf-8")).split("\n")
	default_status='<a class="text-danger">暂无</a>'
	count = 0
	#解决首页项目次数累加,实现根据项目名查询组名
	self.db.hset("progame_to_group",pro_name,select_group)
	self.db.hset(select_group, pro_name, {"count":count,"config":[default_status,default_status,default_status,default_status]})
        #创建工作的根目录
	if self.db.exists("base_path"):  
	    base_path =self.db.get("base_path")
	else:
	    base_path ="/data"
	if not os.path.exists(base_path): os.mkdir(base_path)
	if not os.path.exists("%s/workspaces/"%base_path) : os.makedirs("%s/workspaces/"%base_path)
	os.makedirs("%s/workspaces/%s"%(base_path,pro_name))
	git_clone(git_addr,os.path.join(base_path,"workspaces",pro_name),"127.0.0.1")
	if not self.db.exists(pro_name):
	    self.db.rpush( pro_name, pro_desc, git_addr, str(exec_shell_1), str(exec_shell_2), ssh_server, local_path, remove_path, remote_path,mail_name, mail_subject, str(mail_data), str(remote_exec_shell))
	    self.write("提交成功")
	else:
	    self.write("此工程项目已经存在")

class Add_Group_Handler(BaseHandler):
    '''
    增加分组到REDIS的hash
    '''
    def post(self):
        Group_Name = self.get_argument("Group_Name")
        Group_Desc = self.get_argument("Group_Desc")
	gro_dict={}
	gro_dict[Group_Name] = Group_Desc
	G_redis_name="PROJECT_NAME"
	if self.db.rpush(G_redis_name,gro_dict):
	    self.write("提交成功")
class Exec_Build_Handler(BaseHandler):
    '''
    任务构建执行主函数
    '''
    def post(self):
	sys_cur_dir = os.getcwd()

        G_Name = self.get_argument("G_Name")
        select_result = self.get_argument("select_result")
	get_config = self.db.lrange(G_Name,0,-1)
        if self.db.exists("base_path"):
            base_path = self.db.get("base_path")
        else:
            base_path ="/data"
	#script_before
	if not os.path.exists("tmp"):   os.mkdir("tmp")
	f=open('./tmp/before.sh','a')
	for shell in list(eval(get_config[2])): f.write( shell + "\n")
	f.close()
	#script_after
	f=open('./tmp/after.sh','a')
	for item in list(eval(get_config[3])): f.write( item + "\n")
	f.close()
	#exec_remote_shell
	f=open('./tmp/remote.sh','a')
	for item in list(eval(get_config[11])): f.write( item + "\n")
	f.close()
	#emali data
	f=open('./tmp/email_data.txt','a')
	for item in list(eval(get_config[10])): f.write( item + "\n")
	f.close()
	#获取web  server 地址
        web_server = get_config[4]
	#获取源文件路劲
	src_path = "%s/workspaces/%s"%(base_path,G_Name) +'/'+get_config[5]
	

	#切换到工程目录，准备构建
        os.chdir("%s/workspaces/%s"%(base_path,G_Name))
        #切换分支或者标签或者tag
        git_cmd ='git checkout -f %s'%select_result
        git_data = os.popen(git_cmd).readlines()
	
	#先在本地目录执行构建之前的shell_1脚本
	shell_scripts(os.path.join(sys_cur_dir +"/tmp/","before.sh"),"127.0.0.1")

        #目的机web根路径
        if get_config[6]:
            dest_path = get_config[7]
        else:
            desc_path = get_config[7]+(os.path.dirname(get_config[5]))
        upload_directory(src_path,dest_path,web_server)
	shell_scripts(os.path.join(sys_cur_dir +"/tmp/","remote.sh"),web_server)


	#在本地目录执行构建之后的shell_2脚本
	shell_scripts(os.path.join(sys_cur_dir +"/tmp/","after.sh"),"127.0.0.1")




	#切回mastet
	git_cmd ='git checkout -f master' 
        git_data = os.popen(git_cmd).readlines()
	self.db.hset("history_hash",time.time(),"操作员%s在%s客户端%s发布了%s"%( self.current_user,
									GetNowTime(), 
									self.request.remote_ip, G_Name))
	#删除临时目录tmp
	shutil.rmtree(sys_cur_dir +"/tmp")
	#发送邮件配置
	smtp_info = eval(self.db.get("smtp_eamil"))
	print smtp_info
        try:
            subject = ''.join(get_config[9])
            content = ''.join(get_config[10])
            mail = Mail(     ''.join(smtp_info['smtp_server']), 
			     ''.join(smtp_info['smtp_account']), 
			     ''.join(smtp_info['smtp_passwd']))
            tolist = [get_config[8]]
            mail.send(subject, content, tolist)
        except:
	    print "邮件发送失败，请检查"
	print "操作员%s在%s客户端%s发布了%s"%(self.current_user,GetNowTime(), self.request.remote_ip, G_Name)
	group_name = self.db.hget("progame_to_group",G_Name)
        dict = eval(self.db.hget(group_name, G_Name))
        dict["count"] = dict["count"] + 1
	ico ='<img src="/static/image/blue.png" width="30" height="30" style="color: rgb(255, 140, 60); font-size: 27px;">'
	dict["config"] = [ select_result, ico ,time.time(),self.current_user]
        self.db.hset(group_name, G_Name, str(dict)) 
	self.write(G_Name)


class Get_repo_info_Handler(BaseHandler):
    '''
    获取git仓库版本，分支，标签等信息
    '''
    def post(self):
        G_Name = self.get_argument("G_Name")
	self.write(G_Name)

class Schedule_Handler(BaseHandler):
    def get(self):
        self.render('schedule.html') 

class Test_Handler(BaseHandler):
    '''
    测试定义多个本地变量的文件
    '''
    def get(self):
	#第一种   定义变量新方法，利用handler
	self.name = ["CHEN","REN","WAN"]	
	self.title = "这是测试文件内容"
	#第二种   
	title = "第二种测试标题"
	name = ["chen","ren","wan"]
	_dict = { "title" : title , "name" : name }
        self.render('test.html' ,**_dict ) 
class Role_Post_Handler(BaseHandler):
    '''
    增加角色种类 
    '''
    def post(self):
        role_name  = self.get_argument("role_name")
        role_desc  = self.get_argument("role_desc")
	self.db.rpush("user_role",self.request.arguments)
	self.db.hset("userrole_hash",role_name,['<a class="text-danger">无用户,请增加</a>'])
	print self.request.arguments
	self.write(role_name)
class User_Group_Post_Handler(BaseHandler):
    '''
    增加用户组种类 
    '''
    def post(self):
        user_group_name  = self.get_argument("user_group_name")
        user_group_desc  = self.get_argument("user_group_desc")
	self.db.rpush("user_group",self.request.arguments)
	self.db.hset("usergroup_hash",user_group_name,['<a class="text-danger">无用户,请增加</a>'])
	self.write(user_group_name)

class Adduser_post_Handler(BaseHandler):
    '''
    增加新用户 
    '''
    def post(self):
        username  = self.get_argument("username")
	passwd    = self.get_argument("passwd") 
        tel       = self.get_argument("tel") 
        email     = self.get_argument("email") 
        user_desc = self.get_argument("user_desc")
        user_role = self.get_argument("user_role")
        user_sex  = self.get_argument("user_sex")
        user_group  = self.get_argument("user_group")
	self.request.arguments['start_time'] = [time.time()]
	request_dict = self.request.arguments
	password = ''.join(request_dict['passwd'])
	hashed = bcrypt.hashpw(password, bcrypt.gensalt())
	request_dict['passwd']="[%s]"%hashed
	print request_dict 
	self.db.hset("useradd_hash",username,request_dict)	
	if self.db.hexists("usergroup_hash",user_group):
	    user_group_list = eval(self.db.hget("usergroup_hash",user_group))
	else:
	    user_group_list=[]
	user_group_list.append(username)
	self.db.hset("usergroup_hash",user_group,user_group_list)	

        if self.db.hexists("userrole_hash",user_role):
            user_role_list = eval(self.db.hget("userrole_hash",user_role))
        else:
            user_role_list=[]
        user_role_list.append(username)
        self.db.hset("userrole_hash",user_role,user_role_list)


	print  self.request.arguments
	self.write(username)

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))


class Zh_CN_json_Handler(BaseHandler):
    '''
    给history页面返回json
    '''
    def get(self):
        self.render('zh_CN.json') 
class Exec_Detail_Handler(BaseHandler):
    '''执行构建的详细过程输出
    '''
    def get(self):
        self.render('exec_detail.html') 
class Smtp_test_Handler(BaseHandler):
    '''
    测试smtp连接&发送测试邮件
    '''
    def post(self):
        smtp_server  = self.get_argument("smtp_server").encode("utf-8")
        smtp_eamil    = self.get_argument("smtp_email").encode("utf-8")
        smtp_account = self.get_argument("smtp_account").encode("utf-8")
        smtp_passwd  = self.get_argument("smtp_passwd").encode("utf-8")
	try:
    	    subject = '发送邮件测试' 
    	    content = '本邮件由发布系统自动发送测试邮件，请勿回复！！谢谢！！'
	    mail = Mail(smtp_server,smtp_account,smtp_passwd )
	    tolist = [smtp_eamil] 
    	    mail.send(subject, content, tolist) 
	    self.write("系统向测试%s邮箱发送了一封测试邮件，请查看!"%smtp_eamil)
	except:
	   self.write("测试失败，请确认输入是否正确") 

class Smtp_save_Handler(BaseHandler):
    '''
    smtp配置保存
    '''
    def post(self):
        smtp_server  = self.get_argument("smtp_server").encode("utf-8")
        smtp_eamil    = self.get_argument("smtp_email").encode("utf-8")
        smtp_account = self.get_argument("smtp_account").encode("utf-8")
        smtp_passwd  = self.get_argument("smtp_passwd").encode("utf-8")
        self.write("保存成功") if  smtp_server and self.db.set("smtp_eamil",self.request.arguments) else self.write("保存失败")


class Base_path_Handler(BaseHandler):
    '''
    工作目录
    '''
    def post(self):
        work_path  = self.get_argument("work_path").encode("utf-8")
	if  work_path:
	    if not os.path.exists(work_path):
		os.makedirs(work_path)
	    self.db.set("base_path",work_path)
	    self.write("保存成功")
	else:
	    self.write("不能为空")


class Git_valid_Handler(BaseHandler):
    '''
    验证git 仓库地址是否有效
    '''
    def post(self):
        git_is_valid = self.get_argument("git_valid").encode("utf-8")
	git_repo ='git ls-remote -h %s >/dev/null 2>&1'%git_is_valid
        p = subprocess.Popen(git_repo, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        self.write("false")  if p.returncode != 0 else  self.write("true")



class Develop_choice_Handler(BaseHandler):
    '''
    首页立即构建时候跳转到默认参数版本设置
    '''
    def get(self,group_name):
	if self.db.exists("base_path"):
            base_path = self.db.get("base_path")
        else:
            base_path ="/data"
	cur_dir = os.getcwd()
	os.chdir("%s/workspaces/%s"%(base_path,group_name))
	execute_command("git pull",cwd="%s/workspaces/%s"%(base_path,group_name),timeout=10,shell=True)
	git_version ='git log --after="4 weeks ago" --pretty=format:"%h - %ad %an  %s" --date=iso'
	git_info = os.popen(git_version).readlines()
	os.chdir(cur_dir)
        _dict = { "group_name" : group_name ,"git_info":git_info }
        self.render('develop_choice.html',**_dict) 

class Get_git_info_Handler(BaseHandler):
    '''
    获取克隆下的代码仓库里的版本,分支,标签等信息
    '''
    def post(self):
        condition = self.get_argument("condition").encode("utf-8")
        group_name = self.get_argument("G_Name").encode("utf-8")
	if self.db.exists("base_path"):
            base_path = self.db.get("base_path")
        else:
            base_path ="/data"
	cur_dir = os.getcwd()
	os.chdir("%s/workspaces/%s"%(base_path,group_name))
	if condition =="git_version":
	    git_cmd ='git log --after="4 weeks ago" --pretty=format:"%h - %ad %an  %s" --date=iso'
	elif condition =="git_tag":
	    git_cmd ='git tag -n'
	else :
	    git_cmd ='git branch -a'
	git_data = os.popen(git_cmd).readlines()
	os.chdir(cur_dir)
	self.write(''.join(git_data))


class Login_Handler(BaseHandler):
    def get(self):
        self.render('login.html') 
    def post(self):
	name = self.get_argument("login_username")
	if self.db.hexists("useradd_hash",name):
	    password = self.get_argument("login_password").encode("utf-8")
	    hashed  = (eval((self.db.hget("useradd_hash",name)))['passwd']).strip("[]")
	    if bcrypt.hashpw(password, hashed) == hashed:
    		self.set_secure_cookie("user", name)
    		self.write("ok")
    		
    	    else:
    		self.write("密码不对")
	else:
    	    self.write("用户不对")

class Logout_Handler(BaseHandler):
    def get(self):
	self.set_secure_cookie("user"," ")
     	self.clear_cookie("user")
     	self.redirect('/login/', permanent=True)

class User_data_Handler(BaseHandler):
    '''
    用户资料修改
    '''
    def get(self):
        self.render('user_data.html') 
class ProgrammeEdit_Handler(BaseHandler):
    ''' 
    具体进行修改
    ''' 
    def get(self):
        data = self.db.lrange("PROJECT_NAME",0,-1)
        host_list = get_host_list(pattern="all")
        self.render('programmeEdit.html', data = data, host_list = host_list)




class Ssh_add_Handler(BaseHandler):
    '''
   新增加ssh机器 
    '''
    def post(self):
        G_Name = self.get_argument("host_label")
	print self.request.arguments
	self.write(G_Name)
