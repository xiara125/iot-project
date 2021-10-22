<template>
  <div class="mt-1">
      <div class=" text-left">
          <!-- <span style="font-size:25px; font-weight:bold">{{cityTitle}}</span> -->
          <h3 class="mb-0" style="color :rgba(85, 95, 126, 1);font-weight:bold;">{{cityTitle}}</h3>
          <!-- <img :src="icon" >{{weather.description}} -->
      </div>
      <div class="row" style="text-align:center">
          <div class="col-4">
              <img :src="weather.today.icon"><br>
              {{weather.today.temp}}°
          </div>
          <div class="col-4">
              <img :src="weather.tomorrow.icon"><br>
              {{weather.tomorrow.min_temp}}° / {{weather.tomorrow.max_temp}}°
          </div>
          <div class="col-4">
              <img :src="weather.da_tomorrow.icon"><br>
              {{weather.da_tomorrow.min_temp}}° / {{weather.da_tomorrow.max_temp}}°
          </div>
          <!-- <img :src="icon" >
          <i class="ml-3 mr-2 fas fa-temperature-low"></i>{{weather.today["temp"]}}
          <i class="ml-3 mr-2 fas fa-tint"></i>{{weather.today.humi}}
          <i class="ml-3 mr-2 fas fa-wind"></i>{{weather.today.windSpeed}}
          <i class="ml-3 mr-2 fas fa-location-arrow"></i>{{weather.today.windDeg}} -->
      </div>
  </div>
</template>

<script>
import axios from 'axios'

const APPID = "09e55b3c6482eb81e2895a05b3a8e338"
// const url = "http://api.openweathermap.org/data/2.5/weather"
const url = "http://api.openweathermap.org/data/2.5/onecall"
const units = 'metric'
const lang = 'ko'

export default {
    name: 'Weather',
    props: ['city','cityTitle'],
    data(){
        return {
            weather:{
                'today':{},
                'tomorrow':{},
                'da_tomorrow':{},
            },
            icon: {
                'today':'',
                'tomorrow':'',
                'da_tomorrow':'',
            },
        }
    },
    methods: {
        getWeather(){
            let lat = 37.5683
            let lon = 126.9778
            let exclude = 'hourly,minutely,alerts'
            let params = {lat,lon,exclude,APPID, lang,units}

            let {data} =  axios.get(url,{params})
            console.log(data)

            // this.today ={
            //     main: data.current.weather[0].description,
            //     temp: data.current.temp,
            //     humi: data.current.humidity,
            //     windSpeed: data.current.wind_speed,
            //     windDeg: data.current.wind_deg,
            //     icon : `http://openweathermap.org/img/w/${data.current.weather[0].icon}.png`
            // }
        },
    },
    async mounted(){
        // setInterval(this.getWeather,5000)

        // let q = this.city
        // let params = {q,APPID, lang,units}
        
        let lat = 37.5683
        let lon = 126.9778
        let exclude = 'hourly,minutely,alerts'
        let params = {lat,lon,exclude,APPID, lang,units}

        let {data} = await axios.get(url,{params})
        console.log(data)

        // this.weather ={
        //     main: data.weather[0].description,
        //     temp: data.main.temp,
        //     humi: data.main.humidity,
        //     windSpeed: data.wind.speed,
        //     windDeg: data.wind.deg
        // }
        
        this.weather.today ={
            main: data.current.weather[0].description,
            temp: data.current.temp,
            humi: data.current.humidity,
            windSpeed: data.current.wind_speed,
            windDeg: data.current.wind_deg,
            icon : `http://openweathermap.org/img/w/${data.current.weather[0].icon}.png`
        }
        this.weather.tomorrow ={
            main: data.daily[1].weather[0].description,
            min_temp: data.daily[1].temp.min,
            max_temp: data.daily[1].temp.max,
            icon : `http://openweathermap.org/img/w/${data.daily[1].weather[0].icon}.png`
        }
        this.weather.da_tomorrow ={
            main: data.daily[2].weather[0].description,
            min_temp: data.daily[2].temp.min,
            max_temp: data.daily[2].temp.max,
            icon : `http://openweathermap.org/img/w/${data.daily[2].weather[0].icon}.png`
        }
        console.log(this.weather.today.temp)
        
        // this.icon = `http://openweathermap.org/img/w/${data.weather[0].icon}.png`
        // this.icon = `http://openweathermap.org/img/w/${data.current.weather[0].icon}.png`
    }
}
</script>

<style>

</style>