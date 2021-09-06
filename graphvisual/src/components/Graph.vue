<template>
  <v-container class="flex justify-center mt-2">
    <v-card class="px-4">
      <v-toolbar flat>
        <span class="text-h5">标题</span>
        <v-spacer/>
        <span v-text="'用户ID: '+userid"/>
      </v-toolbar>
      <v-divider/>
      <div v-if="showUserIdEditor">
        <v-card-text style="width:300px">
          <v-text-field
            v-model="userid"
            label="您的用户ID"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn outlined color="grey darken-2" @click="saveUserId" class="mb-8">确认</v-btn>
        </v-card-actions>
      </div>
      <div v-else>
        <div id="graph" :style="{width: '800px', height: '480px'}"></div>
        <v-divider/>
        <v-card-text v-text="text" class="black--text"/>
        <v-card-text>
          <template v-for="(option, index) in options">
            <v-btn :key="index" class="mr-8" outlined color="grey darken-2" @click="returnResult(option)">{{option}}</v-btn>
          </template>
        </v-card-text>
      </div>
    </v-card>
  </v-container>
</template>

<script>
  import * as echarts from 'echarts';
  import axios from 'axios';
  export default {
    data() {
      return {
        userid: null,
        nodes: [],
        edges: [],
        queryid: 0,
        text: null,
        options: ["NULL"],
        showUserIdEditor: true,
      }
    },

    methods: {

      // 保存用户ID，关闭输入框后获取数据
      saveUserId() {
        this.showUserIdEditor = false;
        this.getData();
      },
      
      // 从 Python 后端获取数据
      getData() {
        // 发送Post请求获取数据
        let that = this;
        axios.post('getData', {
          userid: this.userid,
        }).then(function (response) {
          // 写入图数据
          var graph = response.data.graph;
          var inputNodes = graph.nodes;
          var inputEdges =  graph.edges;
          that.nodes = [];
          that.edges = [];
          for (let i in inputNodes) 
            that.nodes.push({name: inputNodes[i]});
          for (let i in inputEdges)
            that.edges.push({source: inputEdges[i][0], target: inputEdges[i][1], label: {show: true, formatter: inputEdges[i][2]}});
          // 绘图
          that.drawGraph();  
          // 更新当前选项
          that.options = response.data.options;
          // 更新当前文本
          that.text = response.data.text;
          // 更新当前查询图的id
          that.queryid = response.data.queryid;
        })
        .catch(function (error) {
          console.log(error);
        });      
      },

      // 向Python后端发送结果
      returnResult(option) {
        let that = this;
        axios.post('returnResult', {
          result: option,
          queryid: this.queryid,
          userid: this.userid
        },{
          headers: {'Content-Type': 'application/json'}
        })
        .then(function (response) {
          console.log(response.data);
          that.getData();
        })
        .catch(function (error) {
          console.log(error);
        });
      },

      // 绘图
      drawGraph() {
        var chartDom = document.getElementById('graph');
        var myChart = echarts.init(chartDom);
        var option;
        option = {
          tooltip: {},
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          series: [{
            type: 'graph',
            layout: 'circular',
            symbolSize: 100,
            roam: true,
            label: {
              show: true,
              width: 100,
              overflow: "break"
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 16],
            edgeLabel: {
              fontSize: 12,
              width: 150,
              overflow: "break"
            },
            data: this.nodes,
            links: this.edges,
            lineStyle: {
              opacity: 0.9,
              width: 2,
            }
          }]
        };
        myChart.setOption(option);
      }
    },

    // 页面加载时的操作
    mounted(){
      this.getData();      
    },

    // 页面变量深度监听，可监听到对象、数组的变化
    watch:{
      options:{
        handler(val){
          this.options = val;
        },
        deep:true     // 深度监听
      },
      userid:{
        handler(val){
          this.userid = val;
        },
        deep:true     // 深度监听
      },
      queryid:{
        handler(val){
          this.queryid = val;
        },
        deep:true     // 深度监听
      },
      text:{
        handler(val){
          this.text = val;
        },
        deep:true     // 深度监听
      },
      nodes:{
        handler(val){
          this.nodes = val;
        },
        deep:true     // 深度监听
      },
      edges:{
        handler(val){
          this.edges = val;
        },
        deep:true     // 深度监听
      },
      showUserIdEditor:{
        handler(val){
          this.showUserIdEditor = val;
        },
        deep:true     // 深度监听
      }
    }
  }
</script>