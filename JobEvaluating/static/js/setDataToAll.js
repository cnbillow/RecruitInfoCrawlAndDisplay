/**
 * Created by Cary on 2016/12/10.
 */

//判定
if (typeof (salary) != "undefined" ){
    showBar();
    $("#display").ready(function(){delete salary;});
}
if (typeof (lan) != "undefined" ){
    var title = "语言热度";
    var desc = ['java', 'python', 'linux', 'php', 'ios', 'android', 'hadoop', 'asp', 'go'];
    showPie(title, desc, lan);
    $("#display").ready(function(){delete lan;});
}

if (typeof (education) != "undefined" ){
    var title = "学历分布";
    var desc = ['中专', '大专',  '应届毕业生', '本科', '研究生', '博士'];
    showPie(title, desc, education);
    $("#display").ready(function(){delete education;});
}



if (typeof (citys) != "undefined"){
    showChinaMap();
    $("#display").ready(function(){delete citys;});

}
if (typeof (ask) != "undefined"){
    showWordle();
    $("#display").ready(function(){delete ask;});
}
if (typeof (heat_lan) != "undefined"){
    showHeat();
   $("#display").ready(function(){delete heat_lan;});
}
