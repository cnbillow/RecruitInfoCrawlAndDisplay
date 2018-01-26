//地图
function showChinaMap(){
	$(document).ready(function(){
			var myChart = echarts.init(document.getElementById('display'));
			var data = citys;
			var geoCoordMap = {
				'广州':[113.23,23.16],'北京':[116.46,39.92], '哈尔滨':[126.63,45.75], '杭州':[120.19,30.26],
				'福州':[119.3,26.08], '武汉':[114.31,30.52], '济南':[117,36.65],
				'昆明':[102.73,25.04], '深圳':[114.07,22.62], '成都':[104.06,30.67],
				'兰州':[103.73,36.03], '乌鲁木齐':[87.68,43.77], '上海':[121.48,31.22],'南宁':[108.33,22.84], '南昌':[115.89,28.68],
				'天津':[117.2,39.13],'银川':[106.27,38.47],'长春':[125.35,43.88], '呼和浩特':[111.65,40.82],
				'重庆':[106.54,29.59],'南京':[118.78,32.04],'郑州':[113.65,34.76],
				'石家庄':[114.48,38.03], '合肥':[117.27,31.86], '长沙':[113,28.21], '西安':[108.95,34.27],
				'沈阳':[123.38,41.8], '海口':[110.35,20.02], '贵阳':[106.71,26.57],'拉萨':[91.11,29.97],
			};

			var convertData = function (data) {
				var res = [];
				for (var i = 0; i < data.length; i++) {
					var geoCoord = geoCoordMap[data[i].name];
					if (geoCoord) {
						res.push({
							name: data[i].name,
							value: geoCoord.concat(data[i].value)
						});
					}
				}
				return res;
			};

			option = {
				backgroundColor: '#404a59',
				title: {
					text: '全国主要城市求职热度图',
					left: 'center',
					textStyle: {
						color: '#fff'
					}
				},
				tooltip : {
					trigger: 'item'
				},
				legend: {
					orient: 'vertical',
					y: 'bottom',
					x:'right',
					data:['工作热度'],
					textStyle: {
						color: '#fff'
					}
				},
				geo: {
					map: 'china',
					label: {
						emphasis: {
							show: false
						}
					},
					roam: true,
					itemStyle: {
						normal: {
							areaColor: '#323c48',
							borderColor: '#111'
						},
						emphasis: {
							areaColor: '#2a333d'
						}
					}
				},
				series : [
					{
						name: '工作热度',
						type: 'scatter',
						coordinateSystem: 'geo',
						data: convertData(data),
						symbolSize: function (val) {
							return val[2] / 300;
						},
						label: {
							normal: {
								formatter: '{b}',
								position: 'right',
								show: false
							},
							emphasis: {
								show: true
							}
						},
						itemStyle: {
							normal: {
								color: '#ddb926'
							}
						}
					},
					{
						name: 'Top 5',
						type: 'effectScatter',
						coordinateSystem: 'geo',
						data: convertData(data.sort(function (a, b) {
							return b.value - a.value;
						}).slice(0, 6)),
						symbolSize: function (val) {
							return val[2] / 1000;
						},
						showEffectOn: 'render',
						rippleEffect: {
							brushType: 'stroke'
						},
						hoverAnimation: true,
						label: {
							normal: {
								formatter: '{b}',
								position: 'right',
								show: true
							}
						},
						itemStyle: {
							normal: {
								color: '#f4e925',
								shadowBlur: 10,
								shadowColor: '#333'
							}
						},
						zlevel: 1
					}
				]
			};


			myChart.setOption(option);
	});
}

//饼状图
function showPie(title, desc, data){
	$(document).ready(function(){
		var myChart = echarts.init(document.getElementById('display'));
		option = {
			title : {
				text: title,
				x:'center'
			},
			tooltip : {
				trigger: 'item',
				formatter: "{a} <br/>{b} : {c} ({d}%)"
			},
			legend: {
				orient: 'vertical',
				left: 'left',
				data: desc,
			},
			series : [
				{
					name: '数据',
					type: 'pie',
					radius : '55%',
					center: ['50%', '60%'],
					data: data,
					itemStyle: {
						emphasis: {
							shadowBlur: 10,
							shadowOffsetX: 0,
							shadowColor: 'rgba(0, 0, 0, 0.5)'
						}
					}
				}
			]
		};
		myChart.setOption(option);
	});
}

//柱状图
function showBar(){
	$(document).ready(function(){
		var myChart = echarts.init(document.getElementById('display'));

		option = {
			title: {
				text: '工资分布图'
			},
			color: ['#3398DB'],
			tooltip : {
				trigger: 'axis',
				axisPointer : {            // 坐标轴指示器，坐标轴触发有效
					type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
				}
			},
			legend: {
				data:['薪资']
			},
			 toolbox: {
				show : true,
				feature : {
					mark : true,
					dataView : {readOnly: false},
					magicType:['line', 'bar'],
					restore : true,
					saveAsImage : true
				}
			},
			calculable : true,
			grid: {
				left: '3%',
				right: '4%',
				bottom: '3%',
				containLabel: true
			},
			xAxis : [
				{
					type : 'category',
					data : ['2000-4000', '4000-6000', '6000-8000', '8000-10000', '10000以上', '面议'],
					axisTick: {
						alignWithLabel: true
					}
				}
			],
			yAxis : [
				{
					type : 'value'
				}
			],
			series : [
				{
					name:'数据量',
					type:'bar',
					barWidth: '60%',
					data: salary,
				}
			]
		};


		 myChart.setOption(option);
	});

}

//词云图
function showWordle(){
	$(document).ready(function(){
		   var myChart = echarts.init(document.getElementById('display'));
        option = {
            title:{
                text:"要求图",
				x:'center'
            },
            tooltip: {},
            series: [{
                type: 'wordCloud',
                gridSize: 20,
                sizeRange: [12, 50],
                rotationRange: [0, 0],
                shape: 'circle',
                textStyle: {
                    normal: {
                        color: function() {
                            return 'rgb(' + [
                                Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160),
                                Math.round(Math.random() * 160)
                            ].join(',') + ')';
                        }
                    },
                    emphasis: {
                        shadowBlur: 10,
                        shadowColor: '#333'
                    }
                },
                data: ask,
			}]
        };
        myChart.setOption(option);
	});

}


//不同工作在个地区的热度图
function showHeat(){
	$(document).ready(function(){
			var myChart = echarts.init(document.getElementById('display'));
			var data = heat_lan;
			var geoCoordMap = {
				'广州':[113.23,23.16],'北京':[116.46,39.92], '哈尔滨':[126.63,45.75], '杭州':[120.19,30.26],
				'福州':[119.3,26.08], '武汉':[114.31,30.52], '济南':[117,36.65],
				'昆明':[102.73,25.04], '深圳':[114.07,22.62], '成都':[104.06,30.67],
				'兰州':[103.73,36.03], '乌鲁木齐':[87.68,43.77], '上海':[121.48,31.22],'南宁':[108.33,22.84], '南昌':[115.89,28.68],
				'天津':[117.2,39.13],'银川':[106.27,38.47],'长春':[125.35,43.88], '呼和浩特':[111.65,40.82],
				'重庆':[106.54,29.59],'南京':[118.78,32.04],'郑州':[113.65,34.76],
				'石家庄':[114.48,38.03], '合肥':[117.27,31.86], '长沙':[113,28.21], '西安':[108.95,34.27],
				'沈阳':[123.38,41.8], '海口':[110.35,20.02], '贵阳':[106.71,26.57],'拉萨':[91.11,29.97],
			};

			var convertData = function (data) {
				var res = [];
				for (var i = 0; i < data.length; i++) {
					var geoCoord = geoCoordMap[data[i].name];
					if (geoCoord) {
						res.push({
							name: data[i].name,
							value: geoCoord.concat(data[i].value)
						});
					}
				}
				return res;
			};

			option = {
				backgroundColor: '#404a59',
				title: {
					text: title+'在不同地区的热度',
					left: 'center',
					textStyle: {
						color: '#fff'
					}
				},
				tooltip : {
					trigger: 'item'
				},
				legend: {
					orient: 'vertical',
					y: 'bottom',
					x:'right',
					data:['工作热度'],
					textStyle: {
						color: '#fff'
					}
				},
				geo: {
					map: 'china',
					label: {
						emphasis: {
							show: false
						}
					},
					roam: true,
					itemStyle: {
						normal: {
							areaColor: '#323c48',
							borderColor: '#111'
						},
						emphasis: {
							areaColor: '#2a333d'
						}
					}
				},
				series : [
					{
						name: '工作热度',
						type: 'scatter',
						coordinateSystem: 'geo',
						data: convertData(data),
						symbolSize: function (val) {
							return val[2] / 10;
						},
						label: {
							normal: {
								formatter: '{b}',
								position: 'right',
								show: false
							},
							emphasis: {
								show: true
							}
						},
						itemStyle: {
							normal: {
								color: '#ddb926'
							}
						}
					},
					{
						name: 'Top 5',
						type: 'effectScatter',
						coordinateSystem: 'geo',
						data: convertData(data.sort(function (a, b) {
							return b.value - a.value;
						}).slice(0, 6)),
						symbolSize: function (val) {
							return val[2] / 10;
						},
						showEffectOn: 'render',
						rippleEffect: {
							brushType: 'stroke'
						},
						hoverAnimation: true,
						label: {
							normal: {
								formatter: '{b}',
								position: 'right',
								show: true
							}
						},
						itemStyle: {
							normal: {
								color: '#800080',
								shadowBlur: 10,
								shadowColor: '#333'
							}
						},
						zlevel: 1
					}
				]
			};


			myChart.setOption(option);
	});
}