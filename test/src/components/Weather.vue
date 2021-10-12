<template>
  <div class="my-3">
      <div class="pl-3 text-left">
          <span style="font-size:2em; font-weight:bold">{{cityTitle}}</span>
          <img :src="icon" >{{weather.description}}
      </div>
      <div>
          <i class="ml-3 mr-2 fas fa-temperature-low"></i>{{weather.temp}}
          <i class="ml-3 mr-2 fas fa-tint"></i>{{weather.humi}}
          <i class="ml-3 mr-2 fas fa-wind"></i>{{weather.windSpeed}}
          <i class="ml-3 mr-2 fas fa-location-arrow"></i>{{weather.windDeg}}
      </div>
  </div>
</template>

<script>
import axios from 'axios'

const APPID = "09e55b3c6482eb81e2895a05b3a8e338"
const url = "http://api.openweathermap.org/data/2.5/weather"
const units = 'metric'
const lang = 'ko'

export default {
    name: 'Weather',
    props: ['city','cityTitle'],
    data(){
        return {
            weather:{},
            icon: '',
        }
    },
    async mounted(){
        let q = this.city
        let params = {q,APPID, lang,units}
        let {data} = await axios.get(url,{params})
        this.weather ={
            main: data.weather[0].description,
            temp: data.main.temp,
            humi: data.main.humidity,
            windSpeed: data.wind.speed,
            windDeg: data.wind.deg
        }
        this.icon = `http://openweathermap.org/img/w/${data.weather[0].icon}.png`
    }
}
</script>

<style>

</style>