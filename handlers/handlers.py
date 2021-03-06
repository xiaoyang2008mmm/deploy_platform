from views.views import *
import os.path

STATIC_PATH   = os.path.join(os.path.dirname(__file__), "../static")
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../templates")
HANDLERS =[(r"/develop/" ,Develop_Handler),
	   (r"/view/",View_Handler),
	   (r"/role/",Role_Handler),
	   (r"/user_group/",User_Group_Handler),
	   (r"/history/",History_Handler),
	   (r"/system/",System_Handler),
	   (r"/login/",Login_Handler),
	   (r"/base/",Base_Handler),
           (r"/logout/", Logout_Handler), 
	   (r"/ssh_page/",Ssh_Page_Handler),
	   (r"/ssh_add/",Ssh_add_Handler),
	   (r"/user/",User_Handler),
	   (r"/user_data/userinfo=(.*)/",User_data_Handler),
	   (r"/charts/",ChartHandler),
	   (r"/programme_edit/programme_name=(.*)/",ProgrammeEdit_Handler),
	   (r"/schedule/",Schedule_Handler),
	   (r"/exec_build/",Exec_Build_Handler),
	   (r"/get_repo_info/",Get_repo_info_Handler),
	   (r"/develop_choice/group_name=(.*)/",Develop_choice_Handler),
	   (r"/get_git_info/",Get_git_info_Handler),
	   (r"/exec_detail/",Exec_Detail_Handler),
	   (r"/post_view/",Post_View_Handler),
	   (r"/role_post/",Role_Post_Handler),
	   (r"/user_group_post/",User_Group_Post_Handler),
	   (r"/add_group/",Add_Group_Handler),
	   (r"/adduser_post/",Adduser_post_Handler),
	   (r"/all/(.*)/",All_Handler),
	   (r"/",Index_Handler),
	   (r"/test/",Test_Handler),
	   (r"/smtp_test/",Smtp_test_Handler),
	   (r"/smtp_save/",Smtp_save_Handler),
	   (r"/base_path/",Base_path_Handler),
	   (r"/git_valid/",Git_valid_Handler),
	   (r"/zh_CN_json/",Zh_CN_json_Handler),
	]
HANDLERS +=[(r"/chart/", ChartHandler)]
