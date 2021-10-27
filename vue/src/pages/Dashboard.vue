<template>
  <div class="pa-5">
    <div class="row">
      <div class="col-4">
        <card>
          <template slot="header">
            <div class="row">
              <div class="col-sm-6" :class="isRTL ? 'text-right' : 'text-left'">
                <h3 class="card-title">{{new Date() | moment("M. D. ddd")}}</h3>
              </div>
            </div>
          </template>
          <div  class="hour" @click="hourState()">
            {{clock.hour}}
          </div>
          <div class="min">
            {{clock.min}}
          </div>
        </card>
        <card>
          <weather city="seoul" cityTitle="Seoul"></weather>
        </card>

        <card >
          <div v-for="(devices,place) in sensors" :key="place" @click="sensorchart = true">
            <h3 style="color :rgba(85, 95, 126, 1);font-weight:bold">{{place}}</h3>
            <div class="row">  
              <div class="col-4"
                v-for="(value, device) in devices" :key="device">
                <Temperature v-if="device==='temp'" :value="value"></Temperature>
                <Humidity v-if="device==='humi'" :value="value"></Humidity>
                <Illusion v-if="device==='illu'" :value="value"></Illusion>
              </div>
            </div>
          </div>
        </card>
      </div>
      <div class="col-8" >
        <card style="height: 677px; font-size : 40px" class="text-center">
          <div class="row" style="margin-top:130px">
            <div class="col-4" style="height: 50px">
              <!-- <router-link :to="{path:'/icons'}"><i class="tim-icons icon-chat-33"></i></router-link> -->
              <span class="material-icons md-inactive md-dark" style="font-size:60px" v-on:click="kitchenLight" v-if="kState==false">light</span>
              <span class="material-icons " style="font-size:60px"  v-on:click="kitchenLight" v-if="kState==true">light</span>
              <!-- <span  style="line-height:1px"><br></span> -->
              <div class="mt-0" style="line-height:10px">
                <span class="room" sytle="opacity:0.2">Kitchen</span>
              </div>
              
            </div>
            <div class="col-4">
                <span class="material-icons md-inactive md-dark" style="font-size:60px" v-on:click="livingRoomLight" v-if="lState==false">light</span>
                <span class="material-icons " style="font-size:60px"  v-on:click="livingRoomLight" v-if="lState==true">light</span>
                <div class="mt-0" style="line-height:10px">
                <span class="room" sytle="opacity:0.2">LivingRoom</span>
              </div>
            </div>
            <div class="col-4">
              <span class="material-icons md-inactive md-dark" style="font-size:60px" v-on:click="bedRoomLight" v-if="bState==false">light</span>
              <span class="material-icons " style="font-size:60px"  v-on:click="bedRoomLight" v-if="bState==true">light</span>
              <div class="mt-0" style="line-height:10px">
                <span class="room" sytle="opacity:0.2">BedRoom</span>
              </div>

            </div>
          </div>
          <div class="row" style="margin-top:100px">
            <div class="col-4" style="height: 50px">
              <div class="myicon">
                <span class="material-icons" style="font-size:60px" @click="lightOff()">flash_off</span>
              </div>
              
            </div>
            <div class="col-4" style="height: 50px">
              <div class="myicon">
              <span class="material-icons" style="font-size:60px" @click="callElevator()">elevator</span>
                <div class="mt-0" style="line-height:10px;">
                <span style="font-size:35px">{{elevator.floor}}</span>
              </div>
                </div>
            </div>
            <div class="col-4">
              <div class="myicon">
              <span class="material-icons" style="font-size:60px" @click="searchModalVisible = true">videocam</span>
              </div>
            </div>
          </div>
          <div class="row" style="margin-top:100px">
            <div class="col-12">
              <div class="myicon">
              <i class="fas fa-microphone" @click="speechToText=true, timeCheck(6000),callSTT()"></i></div>
            </div>
          </div>
        </card>
      </div>
    </div>

    
    <!-- <div class="row">
      <div class="col-lg-4" :class="{'text-right': isRTL}">
        <card type="chart">
          <template slot="header">
            <h5 class="card-category">{{$t('dashboard.completedTasks')}}</h5>
            <h3 class="card-title"><i class="tim-icons icon-send text-success "></i> 센서 데이터</h3>
          </template>
          <div class="chart-area">
            <line-chart style="height: 100%"
                        chart-id="green-line-chart"
                        :chart-data="greenLineChart.chartData"
                        :gradient-stops="greenLineChart.gradientStops"
                        :extra-options="greenLineChart.extraOptions">
            </line-chart>
          </div>
        </card>
      </div>
    </div>  -->
    <!-- <base-button @click="choiceChart = 'temp',showChart()">온도</base-button>
    <base-button @click="choiceChart = 'humi',showChart() ">습도</base-button>
    <base-button @click="choiceChart = 'illu',showChart() ">조도</base-button> -->
    
    <modal :show.sync="sensorchart" 
      id="searchModal"
      :centered="false"
      :show-close="true">
      <template slot="header">
        <h3 class="modal-title">센서 데이터 모니터링</h3>
      </template>

      <!-- <h6 slot="header" class="modal-title" id="modal-title-default">Type your modal title</h6> -->
    <div>
      <card type="chart">
          <template slot="header">
            <h4 class="card-title" v-if="choiceChart=='illu'" >조도</h4>
            <h4 class="card-title" v-if="choiceChart=='temp'" >온도</h4>
            <h4 class="card-title" v-if="choiceChart=='humi'" >습도</h4>
            <!-- <h3 class="card-title"><i class="tim-icons icon-send text-success "></i> 센서 데이터</h3> -->
          </template>
          <div class="chart-area">
            <line-chart style="height: 100%"
                        chart-id="green-line-chart"
                        :chart-data="greenLineChart.chartData"
                        :gradient-stops="greenLineChart.gradientStops"
                        :extra-options="greenLineChart.extraOptions">
            </line-chart>
          </div>
        </card>

    </div>
        <base-button @click="choiceChart = 'temp',showChart()">온도</base-button>
      <base-button @click="choiceChart = 'humi',showChart() ">습도</base-button>
      <base-button @click="choiceChart = 'illu',showChart() ">조도</base-button>
    </modal>


    <modal :show.sync="searchModalVisible" 
      id="searchModal"
      :centered="false"
      :show-close="true">
      <template slot="header">
        <h2 class="modal-title">Camera</h2>
      </template>

      <!-- <h6 slot="header" class="modal-title" id="modal-title-default">Type your modal title</h6> -->
    <div>
      <img :src="streamurl" class="mjpeg" />
    </div>
        <base-button class="animation-on-hover" @click="opendoor()">문 열기</base-button>
        <base-button class="animation-on-hover" @click="closedoor()">문 닫기</base-button>
        <base-button class="animation-on-hover" @click="callInterphone()">인터폰</base-button>
        <base-button class="animation-on-hover" @click="faceCap()">얼굴 인식</base-button>
        <span>  {{capPercent}}</span>
    </modal>

    <modal :show.sync="speechToText"
      
      id="sttModal"
      :centered="false"
      :show-close="true"
      :duration="3000">
      <template slot="header">
        <h2 class="modal-title">음성인식</h2>
      </template>
      <div>
        음성인식 중
      </div>
    </modal>
  </div>
</template>
<script>
  import LineChart from '@/components/Charts/LineChart';
  import BarChart from '@/components/Charts/BarChart';
  import * as chartConfigs from '@/components/Charts/config';
  import TaskList from './Dashboard/TaskList';
  import UserTable from './Dashboard/UserTable';
  import config from '@/config';
  import NotificationTemplate from './Notifications/NotificationTemplate';
  import { BaseAlert } from '@/components';
  import End from './Notifications/End.vue';
  import Start from './Notifications/Start.vue';
  import EarthShake from './Notifications/EarthShake.vue';
  import Modal from '@/components/Modal';
  import Open from './Notifications/Open.vue';
  import Close from './Notifications/Close.vue';
  import LedOff from './Notifications/LedOff.vue';


  let now = new Date()
  let prehour = now.getHours()<10 ? `0${now.getHours()}` : now.getHours()
  let premin = now.getMinutes()<10 ? `0${now.getMinutes()}` : now.getMinutes()
  
  export default {
    components: {
      LineChart,
      BarChart,
      TaskList,
      UserTable,
      BaseAlert,
      Modal,
      
    },
    data() {
      return {
        capPercent:'',
        hState:false,   // 시간 표시 상태
        kState:false,   // kitchen led on/off
        lState:false,   // livingRoom led on/off
        bState:false,   // bedRoom led on/off
        streamurl : 'http://192.168.35.71:8000/mjpeg/stream/',
        speechToText: false,
        activeNotifications: false,
        showMenu: false,
        sensorchart : false,
        searchModalVisible: false,
        searchQuery: '',
        type: ["", "info", "success", "warning", "danger"],
        notifications: {
          topCenter: false
        },
        thLabal:['-80s', '-60s', '-40s', '-20s', 'now'],
        illuLabel:['-12s', '-9s', '-6s', '-3s', 'now'],
        illuCount:0,
        choiceChart:'illu',
        aryillu:[],
        aryhumi:[],
        arytemp:[],
        elevator:{
          floor:'',
          arrive:0
        },
        clock:{
          hour: prehour,
          min : premin,
        },
        sensors:{
          // Room:{
          //   'temp': '',
          //   'humi': '',
          //   // 'illu': '',
          // },
        },
        // bigLineChart: {
        //   allData: [
        //     [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
        //     [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
        //     [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130]
        //   ],
        //   activeIndex: 0,
        //   chartData: {
        //     datasets: [{ }],
        //     labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        //   },
        //   extraOptions: chartConfigs.purpleChartOptions,
        //   gradientColors: config.colors.primaryGradient,
        //   gradientStops: [1, 0.4, 0],
        //   categories: []
        // },
        // purpleLineChart: {
        //   extraOptions: chartConfigs.purpleChartOptions,
        //   chartData: {
        //     labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        //     datasets: [{
        //       label: "Data",
        //       fill: true,
        //       borderColor: config.colors.primary,
        //       borderWidth: 2,
        //       borderDash: [],
        //       borderDashOffset: 0.0,
        //       pointBackgroundColor: config.colors.primary,
        //       pointBorderColor: 'rgba(255,255,255,0)',
        //       pointHoverBackgroundColor: config.colors.primary,
        //       pointBorderWidth: 20,
        //       pointHoverRadius: 4,
        //       pointHoverBorderWidth: 15,
        //       pointRadius: 4,
        //       data: [80, 100, 70, 80, 120, 80],
        //     }]
        //   },
        //   gradientColors: config.colors.primaryGradient,
        //   gradientStops: [1, 0.2, 0],
        // },
        greenLineChart: {
          extraOptions: chartConfigs.greenChartOptions,
          chartData: {
            labels: [],
            datasets: [{
              
              fill: true,
              borderColor: config.colors.danger,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.danger,
              pointBorderColor: 'rgba(255,255,255,0)',
              pointHoverBackgroundColor: config.colors.danger,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data:[]
            }]
          },
          gradientColors: ['rgba(66,134,121,0.15)', 'rgba(66,134,121,0.0)', 'rgba(66,134,121,0)'],
          gradientStops: [1, 0.4, 0],
        },
        // blueBarChart: {
        //   extraOptions: chartConfigs.barChartOptions,
        //   chartData: {
        //     labels: ['USA', 'GER', 'AUS', 'UK', 'RO', 'BR'],
        //     datasets: [{
        //       label: "Countries",
        //       fill: true,
        //       borderColor: config.colors.info,
        //       borderWidth: 2,
        //       borderDash: [],
        //       borderDashOffset: 0.0,
        //       data: [53, 20, 10, 80, 100, 45],
        //     }]
        //   },
        //   gradientColors: config.colors.primaryGradient,
        //   gradientStops: [1, 0.4, 0],
        // }
      }
    },
    computed: {
      enableRTL() {
        return this.$route.query.enableRTL;
      },
      isRTL() {
        return this.$rtl.isRTL;
      },
      bigLineChartCategories() {
        return this.$t('dashboard.chartCategories');
      },
      
    },
    methods: {
      getRandomInt() {
        return Math.floor(Math.random() * (50 - 4)) + 5;
      },
      
      showChart(){
        if(this.choiceChart == 'illu'){
          this.updateChart(this.aryillu,this.illuLabel)
        }
        else if(this.choiceChart == 'humi'){
          this.updateChart(this.aryhumi,this.thLabal)
        }
        else{
          this.updateChart(this.arytemp,this.thLabal)
        }
      },
      updateChart(arydata,arylabel){
        let chartData ={
          labels: arylabel,
          datasets:[{
            
            fill: true,
            borderColor: config.colors.danger,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.danger,
            pointBorderColor: 'rgba(255,255,255,0)',
            pointHoverBackgroundColor: config.colors.danger,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data:arydata,
          }]
        }
        this.greenLineChart.chartData = chartData
      },
      hourState(){
        this.hState==true ? this.hState=false : this.hState=true
        this.getClock()
      },
      turnOffAll(){
        this.$mqtt.publish('iot/hong/led','all')
        this.kState=false
        this.lState=false
        this.bState=false
        this.notifyVue('top','center',LedOff)
      },
      lightOff(){
        setTimeout(this.turnOffAll,3000)
      },
      kitchenLight(){
        this.kState = !this.kState
        this.$mqtt.publish('iot/hong/led',`kitchen/${this.kState}`)
        // console.log(`${this.kState}입니다`)
      },
      livingRoomLight(){
        this.lState = !this.lState
        this.$mqtt.publish('iot/hong/led',`livingRoom/${this.lState}`)
      },
      bedRoomLight(){
        this.bState = !this.bState
        this.$mqtt.publish('iot/hong/led',`bedRoom/${this.bState}`)
      },
      faceCap(){
        this.$mqtt.publish('iot/hong/face/capture','call')
      },
      timeCheck(time){
        // setTimeout(this.timeout,5000)
        setTimeout(this.timeout,time)
      },
      timeout(){
        this.searchModalVisible=false
        this.speechToText=false
      },
      consoleTest(){
        console.log('테스트')
      },
      opendoor(){
        this.$mqtt.publish('iot/hong/door','open')
      },
      closedoor(){
        this.$mqtt.publish('iot/hong/door','close')
      },
      notifyVue(verticalAlign, horizontalAlign,component) {
        const color = Math.floor(Math.random() * 4 + 1);
        this.$notify({
          component: component,
          icon: "tim-icons icon-bell-55",
          horizontalAlign: horizontalAlign,
          verticalAlign: verticalAlign,
          type: this.type[color],
          timeout: 5000
        });
      },
      getClock(){
        let gettime = new Date()

        if(this.hState == true){  // 12 표시
          let h = gettime.getHours()
          h = h>12? h-12:h
          this.hour = h<10 ? `0${h}` : h
        }
        else{   // 24 표시
          this.hour = gettime.getHours() <10 ? `0${gettime.getHours()}` : gettime.getHours()
        }
        
        this.min = gettime.getMinutes()<10 ? `0${gettime.getMinutes()}` : gettime.getMinutes()
        
        this.clock.hour = this.hour
        this.clock.min = this.min
        
      },
      callInterphone(){
        this.$mqtt.publish('iot/hong/interphone','1')
        console.log()
        this.notifyVue('top','center',Start)
      },
      showElevator(){
        this.$mqtt.publish('iot/hong/control/elevator','s')
        console.log()
      },
      callElevator(){
        this.$mqtt.publish('iot/hong/control/elevator','5')
        console.log()
      },
      callSTT(){
        this.$mqtt.publish('iot/hong/STT','call')
        console.log()
      },
      callDHT(){
        this.$mqtt.publish('iot/hong/control/elevator','0')
        this.$mqtt.publish('iot/hong/call/illu','call')
        console.log()
      },
      toggleSidebar() {
        this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
      },
      // initBigChart(index) {
      //   let chartData = {
      //     datasets: [{
      //       fill: true,
      //       borderColor: config.colors.primary,
      //       borderWidth: 2,
      //       borderDash: [],
      //       borderDashOffset: 0.0,
      //       pointBackgroundColor: config.colors.primary,
      //       pointBorderColor: 'rgba(255,255,255,0)',
      //       pointHoverBackgroundColor: config.colors.primary,
      //       pointBorderWidth: 20,
      //       pointHoverRadius: 4,
      //       pointHoverBorderWidth: 15,
      //       pointRadius: 4,
      //       data: this.bigLineChart.allData[index]
      //     }],
      //     labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
      //   }
      //   // this.$refs.bigChart.updateGradients(chartData);
      //   this.bigLineChart.chartData = chartData;
      //   this.bigLineChart.activeIndex = index;
      // },
    },
    mqtt: {
        'iot/hong/floor/elevator': function(value,topic) {
            let [,,,ele] = topic.split('/')
            console.log(ele)
            console.log(value-'0')
            this.elevator.floor = value
            
        },
        'iot/hong/arrive/elevator': function(value,topic) {
            let [,,,ele] = topic.split('/')
            console.log(ele)
            if (value == 1){
              console.log('도착')
              // window.alert('도착!!')
              this.notifyVue('top','center',NotificationTemplate)
            }
            // this.elevator.floor = value
        },
        'iot/hong/interphone': function(value,topic) {
            // console.log(topic)
            if (value == 0){
              console.log('종료')
              // window.alert('도착!!')
              this.notifyVue('top','center',End)
            }
            // this.elevator.floor = value
        },
        'iot/sensors/#': function(value, topic) {
            let [,,place,device] = topic.split('/')
            // // 처음 인식된 장소면 빈 객체 추가
            !this.sensors[place] && (this.sensors[place] = {})
            this.sensors[place][device] = value
            this.sensors={ ...this.sensors  }
            // console.log(device,value-'0')
            // console.log(this.greenLineChart.chartData.datasets[0].data[4])
            // this.greenLineChart.chartData.datasets[0].data[4] = this.sensors[place].temp-'0'
            // this.greenLineChart = {...this.greenLineChart}
            if(device == 'temp'){
              if(this.arytemp.length ==5){
                this.arytemp.shift()
                this.arytemp.push(this.sensors[place].temp-'0')  
              }
              else{
                this.arytemp.push(this.sensors[place].temp-'0')
              }
              
            }
            else if(device == 'humi'){
              if(this.aryhumi.length ==5){
                this.aryhumi.shift()
                this.aryhumi.push(this.sensors[place].humi-'0')  
              }
              else{
                this.aryhumi.push(this.sensors[place].humi-'0')
              }
            }
            else if(device == 'illu'){
              if(this.illuCount == 3){
                this.illuCount = 0
                if(this.aryillu.length ==5){
                  this.aryillu.shift()
                  this.aryillu.push(this.sensors[place].illu-'0')  
                }
                else{
                  this.aryillu.push(this.sensors[place].illu-'0')
                }
              }
              
              this.illuCount += 1 
            }

            if(this.choiceChart == 'temp'){
                this.updateChart(this.arytemp,this.thLabal)
              }
            else if(this.choiceChart == 'humi'){
              this.updateChart(this.aryhumi,this.thLabal)
            }
            else if(this.choiceChart == 'illu'){
              this.updateChart(this.aryillu,this.illuLabel)
            }


            // console.log('조도센서 :',this.aryillu)
            // console.log('온도센서 :',this.arytemp)
            // console.log('습도센서 :',this.aryhumi)
            // console.log('choicechart :',this.choiceChart)
        },
        'iot/earthshake': function(value, topic) {
            if (value == 1){
              console.log('지진발생')
              this.notifyVue('top','center',EarthShake)
            }
            // console.log(topic,value)
        },
        'iot/face/check': function(value, topic) {
            if (value == 'open'){
              console.log('open')
              this.notifyVue('top','center',Open)
            }
            else if(value =='close'){
              console.log('close')
              this.notifyVue('top','center',Close)
            }
        },
        'iot/led/#': function(value, topic) {
            // console.log(topic.split('/'))
            let aryTopic = topic.split('/')
            if(aryTopic[2] == 'kitchen'){
              value == '0'? this.kState = false : this.kState = true
            }
            if(aryTopic[2] == 'livingRoom'){
              value == '0'? this.lState = false : this.lState = true
            }
            if(aryTopic[2] == 'bedRoom'){
              value == '0'? this.bState = false : this.bState = true
            }
        },
        'iot/hong/face/capture': function(value, topic) {
            // console.log(topic)
            if(value == 'start'){
              this.notifyVue('top','center',Start)
              // this.capPercent = '0'
              this.capPercent = '□□□□□□□□'
            }
            else if(value == 'end'){
              this.notifyVue('top','center',End)
              this.capPercent = ''
            }
            else if(value == '25'){
              // console.log('25')
              // this.capPercent = value
              this.capPercent = '■■□□□□□□'
            }
            else if(value == '50'){
              // console.log('50')
              // this.capPercent = value
              this.capPercent = '■■■■□□□□'
            }
            else if(value == '75'){
              // console.log('75')
              // this.capPercent = value
              this.capPercent = '■■■■■■□□'
            }
            console.log(value-'0')
        },
        
    },
    mounted() {
      // this.showElevator()
      // this.fillData()      
      this.i18n = this.$i18n;
      if (this.enableRTL) {
        this.i18n.locale = 'ar';
        this.$rtl.enableRTL();
      }
      // this.initBigChart(0);
      
      // setInterval(this.showChart,500)
    
      // 구독 신청
      this.$mqtt.subscribe('iot/hong/floor/elevator')
      this.$mqtt.subscribe('iot/hong/arrive/elevator')
      this.$mqtt.subscribe('iot/hong/interphone')
      this.$mqtt.subscribe('iot/sensors/#')
      this.$mqtt.subscribe('iot/earthshake')
      this.$mqtt.subscribe('iot/face/check')
      this.$mqtt.subscribe('iot/led/#')
      this.$mqtt.subscribe('iot/hong/face/capture')
      
      

      if(this.min<10){
        this.min = `0${this.min}`
      }

      setInterval(this.getClock,1000)
      // setTimeout(this.callDHT,100)
      // setInterval(,5000)
      this.callDHT()
      this.$mqtt.publish('iot/hong/led','call')

    },
    unmounted() {
        // 구독 해제
        this.$mqtt.unsubscribe('iot/hong/floor/elevator')
        this.$mqtt.subscribe('iot/hong/arrive/elevator')
        this.$mqtt.subscribe('iot/hong/interphone')
        this.$mqtt.subscribe('iot/sensors/#')
    },
    beforeDestroy() {
      if (this.$rtl.isRTL) {
        this.i18n.locale = 'en';
        this.$rtl.disableRTL();
      }
    }
  };
</script>
<style scope>
.hour{
  font-size: 130px;
  color : rgb(211, 202, 255);
  font-weight: lighter;
  font-family: 'Courier New', Courier, monospace;
  line-height: 1em;
  letter-spacing: -20px;
}
.min{
  font-size: 130px;
  color :rgb(210, 210, 210);
  font-weight: 100;
  font-family: 'Courier New', Courier, monospace;
  line-height: 1em;
  letter-spacing: -20px;
}
.weather{
  line-height: 1em;
  padding-top: 0px;
  padding-bottom: 0px;
}
.material-icons.md-dark { color: rgba(0, 0, 0, 0.54); }
.material-icons.md-dark.md-inactive { color: rgba(0, 0, 0, 0.26); }

.material-icons.md-light { color: rgba(255, 255, 255, 1); }
.material-icons.md-light.md-inactive { color: rgba(255, 255, 255, 0.3); }

.room{
  color :rgba(85, 95, 126, 1);
  
  font-size:20px;
  
}
.myicon:active{
   color :rgba(27, 27, 46, 1);

}
</style>
