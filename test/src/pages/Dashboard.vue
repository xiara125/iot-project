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
          <div  class="hour">
            {{clock.hour}}
          </div>
          <div class="min">
            {{clock.min}}
          </div>
        </card>
        <card>
          <weather city="seoul" cityTitle="서울"></weather>
        </card>
        <card>
          <div v-for="(devices,place) in sensors" :key="place">
            <h3>{{place}}</h3>
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
          <div class="row" style="margin-top:200px">
            <div class="col-4">
              <router-link :to="{path:'/icons'}"><i class="tim-icons icon-chat-33"></i></router-link>
            </div>
            <div class="col-4">
                <i slot="title" class="tim-icons icon-bell-55" @click="callElevator()"></i> 
                <br>{{elevator.floor}}
            </div>
            <div class="col-4">
              
              <i slot="title" class="tim-icons icon-button-power" @click="callInterphone()"></i>
            </div>
          </div>
          <div class="row" style="margin-top:100px">
            <div class="col-4">
              <i slot="title" class="tim-icons icon-light-3" @mousedown="callSTT()"></i>
            </div>
            <div class="col-4">
              <i slot="title" class="tim-icons icon-time-alarm"></i>
            </div>
            <div class="col-4">
              <i slot="title" class="tim-icons icon-video-66"></i>
            </div>
          </div>
        </card>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-4" :class="{'text-right': isRTL}">
        <card type="chart">
          <template slot="header">
            <h5 class="card-category">{{$t('dashboard.completedTasks')}}</h5>
            <h3 class="card-title"><i class="tim-icons icon-send text-success "></i> 12,100K</h3>
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
    </div>
    <!-- <div class="row">
      <div class="col-lg-6 col-md-12">
        <card type="tasks" :header-classes="{'text-right': isRTL}">
          <template slot="header">
            <h6 class="title d-inline">{{$t('dashboard.tasks', {count: 5})}}</h6>
            <p class="card-category d-inline">{{$t('dashboard.today')}}</p>
            <base-dropdown menu-on-right=""
                           tag="div"
                           title-classes="btn btn-link btn-icon"
                           aria-label="Settings menu"
                           :class="{'float-left': isRTL}">
              <i slot="title" class="tim-icons icon-settings-gear-63"></i>
              <a class="dropdown-item" href="#pablo">{{$t('dashboard.dropdown.action')}}</a>
              <a class="dropdown-item" href="#pablo">{{$t('dashboard.dropdown.anotherAction')}}</a>
              <a class="dropdown-item" href="#pablo">{{$t('dashboard.dropdown.somethingElse')}}</a>
            </base-dropdown>
          </template>
          <div class="table-full-width table-responsive">
            <task-list></task-list>
          </div>
        </card>
      </div>
      <div class="col-lg-6 col-md-12">
        <card class="card" :header-classes="{'text-right': isRTL}">
          <h4 slot="header" class="card-title">{{$t('dashboard.simpleTable')}}</h4>
          <div class="table-responsive">
            <user-table></user-table>
          </div>
        </card>
      </div>
    </div> -->
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
      
    },
    data() {
      return {
        type: ["", "info", "success", "warning", "danger"],
        notifications: {
          topCenter: false
        },
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
        bigLineChart: {
          allData: [
            [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
            [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
            [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130]
          ],
          activeIndex: 0,
          chartData: {
            datasets: [{ }],
            labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
          },
          extraOptions: chartConfigs.purpleChartOptions,
          gradientColors: config.colors.primaryGradient,
          gradientStops: [1, 0.4, 0],
          categories: []
        },
        purpleLineChart: {
          extraOptions: chartConfigs.purpleChartOptions,
          chartData: {
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
            datasets: [{
              label: "Data",
              fill: true,
              borderColor: config.colors.primary,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              pointBackgroundColor: config.colors.primary,
              pointBorderColor: 'rgba(255,255,255,0)',
              pointHoverBackgroundColor: config.colors.primary,
              pointBorderWidth: 20,
              pointHoverRadius: 4,
              pointHoverBorderWidth: 15,
              pointRadius: 4,
              data: [80, 100, 70, 80, 120, 80],
            }]
          },
          gradientColors: config.colors.primaryGradient,
          gradientStops: [1, 0.2, 0],
        },
        greenLineChart: {
          extraOptions: chartConfigs.greenChartOptions,
          chartData: {
            now_temp : '',
            labels: ['JUL', 'AUG', 'SEP', 'OCT', 'NOV'],
            datasets: [{
              label: "My First dataset",
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
              data: ['20', '27', '30', '42',''],
            }]
          },
          gradientColors: ['rgba(66,134,121,0.15)', 'rgba(66,134,121,0.0)', 'rgba(66,134,121,0)'],
          gradientStops: [1, 0.4, 0],
        },
        blueBarChart: {
          extraOptions: chartConfigs.barChartOptions,
          chartData: {
            labels: ['USA', 'GER', 'AUS', 'UK', 'RO', 'BR'],
            datasets: [{
              label: "Countries",
              fill: true,
              borderColor: config.colors.info,
              borderWidth: 2,
              borderDash: [],
              borderDashOffset: 0.0,
              data: [53, 20, 10, 80, 100, 45],
            }]
          },
          gradientColors: config.colors.primaryGradient,
          gradientStops: [1, 0.4, 0],
        }
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
      updateChart(){

      },
      notifyVue(verticalAlign, horizontalAlign,component) {
        const color = Math.floor(Math.random() * 4 + 1);
        this.$notify({
          component: component,
          icon: "tim-icons icon-bell-55",
          horizontalAlign: horizontalAlign,
          verticalAlign: verticalAlign,
          type: this.type[color],
          timeout: 0
        });
      },
      getClock(){
        let gettime = new Date()
        // this.hour = gettime.getHours()
        // this.min = gettime.getMinutes()
        this.hour = gettime.getHours() <10 ? `0${gettime.getHours()}` : gettime.getHours()
        this.min = gettime.getMinutes()<10 ? `0${gettime.getMinutes()}` : gettime.getMinutes()
        // this.hour = this.hour<10 ? `0${this.hour}`:this.hour
        // this.min = this.min<10 ? `0${this.min}`:this.min
        // if (this.min<10){
        //   this.min = `0${this.min}`
        //   // console.log(this.min)
        // }
        // console.log('현재시간')
        // console.log(this.hour,this.min)
        // console.log(typeof(this.hour))
        this.clock.hour = this.hour
        this.clock.min = this.min
      },
      callInterphone(){
        this.$mqtt.publish('iot/hong/interphone','1')
        console.log()
        this.notifyVue('top','center',Start)
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
      initBigChart(index) {
        let chartData = {
          datasets: [{
            fill: true,
            borderColor: config.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.primary,
            pointBorderColor: 'rgba(255,255,255,0)',
            pointHoverBackgroundColor: config.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: this.bigLineChart.allData[index]
          }],
          labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
        }
        // this.$refs.bigChart.updateGradients(chartData);
        this.bigLineChart.chartData = chartData;
        this.bigLineChart.activeIndex = index;
      },
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
            // this.arytemp.push(this.sensors[place].temp-'0')
            // console.log(this.arytemp)


        },
        'iot/earthshake': function(value, topic) {
            if (value == 1){
              console.log('지진발생')
              this.notifyVue('top','center',EarthShake)
            }
            // console.log(topic,value)
        },
    },
    mounted() {
      this.i18n = this.$i18n;
      if (this.enableRTL) {
        this.i18n.locale = 'ar';
        this.$rtl.enableRTL();
      }
      this.initBigChart(0);
      
      // 구독 신청
      this.$mqtt.subscribe('iot/hong/floor/elevator')
      this.$mqtt.subscribe('iot/hong/arrive/elevator')
      this.$mqtt.subscribe('iot/hong/interphone')
      this.$mqtt.subscribe('iot/sensors/#')
      this.$mqtt.subscribe('iot/earthshake')

      if(this.min<10){
        this.min = `0${this.min}`
      }

      setInterval(this.getClock,1000)
      setTimeout(this.callDHT,100)
      
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

</style>
