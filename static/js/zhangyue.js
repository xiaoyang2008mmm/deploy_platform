$(document).ready(function() {
    $("#view_save").click(function() {
        if ($("#pro_name").val() == "" || $("#git_addr").val() == "") {
            alert("项目名称或git地址不能为空");
        } else {
            alert("正在克隆第一份代码，可能花点时间，请等待.......");
            $.post("/post_view/", {
                pro_name: $("#pro_name").val(),
                pro_desc: $("#pro_desc").val(),
                git_addr: $("#git_addr").val(),
                exec_shell_1: $("#exec_shell_1").val(),
                exec_shell_2: $("#exec_shell_2").val(),
                ssh_server: $("#ssh_server option:selected").text(),
                local_path: $("#local_path").val(),
                remove_path: $("#remove_path").val(),
                remote_path: $("#remote_path").val(),
                mail_name: $("#mail_name").val(),
                mail_subject: $("#mail_subject").val(),
                mail_data: $("#mail_data").val(),
                select_group: $('#select_group option:selected').text(),
                remote_exec_shell: $("#remote_exec_shell").val(),
            },
            function(data) {
                alert(data);
            });
            location.href = '/';
        };
    });

    ///////////////////////////////////////////////////////////////
    $("#git_addr").change(function() {
        if ($("#git_addr").val() == "") {
            alert("git地址不能为空");
        } else {
            $.post("/git_valid/", {
                git_valid: $(this).val(),
            },
            function(data) {
                if (data == "true") {
                    $("#git_message").text("仓库地址可以连接");
                } else {
                    $("#git_message").text("仓库地址连接失败");
                }
            });
        };
    });

    ///////////////////////////////////////////////////////////////
    $("#Group_btn").click(function() {
        if ($("#Group_Name").val() == "") {
            alert("组名字不能为空");
        } else {
            $.post("/add_group/", {
                Group_Name: $("#Group_Name").val(),
                Group_Desc: $("#Group_Desc").val(),
            },
            function(data) {
                alert(data);
            });
            location.href = '/';
        };
    });

    ////////////////////////////////////////////////////////////
    var $groupTabs = $('#myTab li');
    $groupTabs.not(':last').click(function() {
        var group_name = $(this).text();
        if (group_name != "") {
            localStorage.setItem('key_group_name', group_name);
            location.href = '/all/' + group_name + '/';
        }
    });

    function _getCurrentGroup() {
        for (var i = 0; i < $groupTabs.size() - 1; i++) {
            if ($groupTabs.eq(i).text() == localStorage.getItem('key_group_name')) {
                return i
            }
        }
        return 0
    }

    $(function() {
        $groupTabs.eq(_getCurrentGroup()).find('a').tab('show');
    });

    ////////////////////////////////////////////////////////////
    $("#table  td span").click(function() {
        var $G_Name = $(this).parent().parent().children("td").eq(0).children("a").text();
        location.href = '/develop_choice/group_name=' + $G_Name + '/';
    });

    /////////////////////////////////////////////////////////////
    $("#deve_cancel").click(function() {
        location.href = '/';

    });
    ///////////////////////////////////////////////////////////
    $("#deve_sure").click(function() {
        var $G_Name = $("#deve_name").text();
        var $select_id = $('#git_list option:selected').text();
        var $condition = $("#select_condition option:selected").val();
        if ($select_id == "") {
            alert("请选择项目参数!!!!!");
        } else {
            var $select_result = git_args($condition, $select_id);
            post_func($G_Name, $select_result);
        }
    });

    function post_func($G_Name, $select_result) {
        var msg = "确定要立刻构建吗?";
        if (confirm(msg) == true) {
            $.post("/exec_build/", {
                G_Name: $G_Name,
                select_result: $select_result,
            },
            function(data) {
                alert(data);
            });
            location.href = '/schedule/';
        } else {
            return false;
        }

    }

    function git_args($condition, $select_id) {
        var data;
        switch ($condition) {
        case "git_version":
            //alert((($select_id).split("-"))[0]);
            data = (($select_id).split("-"))[0];
            break;
        case "git_tag":
            //alert((($select_id).split(" "))[0]);
            data = (($select_id).split(" "))[0];
            break;
        case "git_branch":
            //alert(($select_id).replace("remotes/origin/",""));
            data = ($select_id).replace("remotes/origin/", "");
            break;
        }
        return data;
    }

    //////////////////////////////////////////////////////////////
    /*view页面span图标点击事件*/
    $("#retu_home").click(function() {
        location.href = '/';
    });

    //////////////////////////////////////////////////////////
    $("#status_detail").click(function() {
        location.href = '/exec_detail/';
    });

    ///////////////////////////////////////////////////////////////
    $("#form1").validation({
        icon: true
    });
    ///////////////////////////////////////////////////////////////
    $("#role_post_button").click(function() {
        if ($("#role_name").val() == "") {
            alert("角色名字不能为空");
        } else {
            $.post("/role_post/", {
                role_name: $("#role_name").val(),
                role_desc: $("#role_desc").val(),
            },
            function(data) {
                alert("保存成功");
                alert(data);
            });
            location.href = '/role/';
        };
    });
    /////////////////////////////////////////////////////////////
    $("#user_group_button").click(function() {
        if ($("#user_group_name").val() == "") {
            alert("用户组名字不能为空");
        } else {
            $.post("/user_group_post/", {
                user_group_name: $("#user_group_name").val(),
                user_group_desc: $("#user_group_desc").val(),
            },
            function(data) {
                alert("保存成功");
                alert(data);
            });
            location.href = '/user_group/';
        };
    });
    //////////////////////////////////////////////////////////
    //验证用户名表单是否为空
    $("#username").mouseleave(function() {
        if ($("#username").val() == "") {
            $("#username").css("background-color", "#FFD2D2"),
            $("#user_error").removeClass("hide");
        };
        if ($("#username").val() != "") {
            $("#username").css("background-color", "white"),
            $("#user_error").addClass("hide");
        };
    });
    $("#passwd-1").mouseleave(function() {
        if ($("#passwd-1").val() == "") {
            $("#passwd-1").css("background-color", "#FFD2D2");
        };
        if ($("#passwd-1").val() != "") {
            $("#passwd-1").css("background-color", "white");
        };
    });
    $("#passwd-2").mouseleave(function() {
        if ($("#passwd-2").val() == "") {
            $("#passwd-2").css("background-color", "#FFD2D2");
        };
        if ($("#passwd-2").val() != "") {
            $("#passwd-2").css("background-color", "white");
        };
    });
    $("#tel").mouseleave(function() {
        if ($("#tel").val() == "") {
            $("#tel").css("background-color", "#FFD2D2");
        };
        if ($("#tel").val() != "") {
            $("#tel").css("background-color", "white");
        };
    });
    $("#email").mouseleave(function() {
        if ($("#email").val() == "") {
            $("#email").css("background-color", "#FFD2D2");
        };
        if ($("#email").val() != "") {
            $("#email").css("background-color", "white");
        };
    });
    //////////////////////////////////////////////////////////////////////
    $("#user_post").click(function() {
        if ($("#username").val() == "") {
            alert("用户名不能为空!!");
        } else if ($("#passwd-1").val() != $("#passwd-2").val()) {
            alert("密码不一致");
        } else {
            $.post("/adduser_post/", {
                username: $("#username").val(),
                passwd: $("#passwd-1").val(),
                tel: $("#tel").val(),
                email: $("#email").val(),
                user_desc: $("#user_desc").val(),
                user_role: $("#user_role option:selected").val(),
                user_group: $("#user_group option:selected").val(),
                user_sex: $('input:radio[name="optionsRadiosinline"]:checked').val(),
            },
            function(data) {
                alert("保存成功");
                alert(data);
            });
            location.href = '/user/';
        };
    });
    //////////////////////////////////////////////////////////////////////
    $("#search_btn").click(function() {
        if ($("#search_keys").val() != "") {
            alert($("#search_keys").val());
            $("#search_tbody tr").hide();
        }
    });

    //////////////////////////////////////////////////////////
    //smtp配置测试连接
    $("#smtp_test").click(function() {
        var $smtp_server = $("#smtp_server").val();
        var $smtp_email = $("#smtp_email").val();
        var $smtp_account = $("#smtp_account").val();
        var $smtp_passwd = $("#smtp_passwd").val();
        $.post("/smtp_test/", {
            smtp_server: $smtp_server,
            smtp_email: $smtp_email,
            smtp_account: $smtp_account,
            smtp_passwd: $smtp_passwd,
        },
        function(data) {
            alert(data);
        });
    });

    //////////////////////////////////////////////////////////
    //smtp配置保存
    $("#smtp_save").click(function() {
        var $smtp_server = $("#smtp_server").val();
        var $smtp_email = $("#smtp_email").val();
        var $smtp_account = $("#smtp_account").val();
        var $smtp_passwd = $("#smtp_passwd").val();
        $.post("/smtp_save/", {
            smtp_server: $smtp_server,
            smtp_email: $smtp_email,
            smtp_account: $smtp_account,
            smtp_passwd: $smtp_passwd,
        },
        function(data) {
            alert(data);
        });
        location.href = '/system/';
    });

    //////////////////////////////////////////////////////////
    $("#path_save").click(function() {
        var $work_path = $("#work_path").val();
        $.post("/base_path/", {
            work_path: $work_path,
        },
        function(data) {
            alert(data);
        });
        location.href = '/system/';
    });
    /////////////////////////////////////////////////////////////
    $("#select_condition").change(function() {
        var $condition = $("#select_condition option:selected").val();
        var $G_Name = $("#deve_name").text();
        $("#git_list").empty();
        $.post("/get_git_info/", {
            condition: $condition,
            G_Name: $G_Name,
        },
        function(data) {
            for (var i = 0; i < (data.split("\n")).length; i++) {
                $("#git_list").append("<option>" + (data.split("\n"))[i] + "</option>");
            }
        });
    });

    //////////////////////////////////////////////////////////
    $("#base_search").change(function() {
        var $search_list = $("#base_search").val();
        alert($search_list);
    });
    //////////////////////////////////////////////////////////
    ///提交ssh信息
    $("#host_test").click(function() {
        var $args = "test";
        if ($("#host_ip").val() == "") {
            $("#host_ip").parent().addClass("has-error");
        } else if ($("#host_path").val() == "") {
            $("#host_path").parent().addClass("has-error");
        } else if ($("#host_key").val() == "") {
            $("#host_key").parent().addClass("has-error");
        } else if ($("#host_port").val() == "") {
            $("#host_port").parent().addClass("has-error");
        } else if ($("#host_ip").val() != "") {
            checkIP($args);
        };
    });
    $("#host_save").click(function() {
        var $args = "save";
        if ($("#host_ip").val() == "") {
            $("#host_ip").parent().addClass("has-error");
        } else if ($("#host_path").val() == "") {
            $("#host_path").parent().addClass("has-error");
        } else if ($("#host_key").val() == "") {
            $("#host_key").parent().addClass("has-error");
        } else if ($("#host_port").val() == "") {
            $("#host_port").parent().addClass("has-error");
        } else if ($("#host_ip").val() != "") {
            checkIP($args);
        };
    });
    function ssh_post($args) {
        var $host_label = $("#host_label").val();
        var $host_ip = $("#host_ip").val();
        var $host_path = $("#host_path").val();
        var $host_key = $("#host_key").val();
        var $host_port = $("#host_port").val();
        var $host_time = $("#host_time").val();
        $.post("/ssh_add/", {
            host_label: $host_label,
            host_ip: $host_ip,
            host_path: $host_path,
            host_key: $host_key,
            host_port: $host_port,
            host_time: $host_time,
            args: $args,
        },
        function(data) {
		if( data=="exist"){
			$('#ssh_error').removeClass("hide");
			$("#ssh_error p").text("SSH 主机已经存在,请检查填写内容");
		}else if( data=="success"){
            		alert("保存成功");
			$("input").val(""); //清空表单数据，防止重复提交
		} else{
            		alert(data);
			}
        });

    }

    function checkIP($args) {
        var $host_ip = $("#host_ip").val();
        var exp = /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
        var reg = $host_ip.match(exp);
        if (reg == null) {
                alert("IP地址不合法！");
        }else{
		alert("IP地址合法！"); 
		ssh_post($args);
	} 
    }



    //////////////////////////////////////////////////////
});
