<template>
  <div>
    <!-- <v-icon x-large class="mr-3 float-left" 
        :color="color">fas {{icon}}</v-icon> -->
    <div  class="font-weight-bold">온도</div>
    <span>{{value}}°C</span>

  </div>
</template>

<script>
export default {
    name: 'Temperature',
    props: ['value'],
    data() {
        return {
            icons: [
                'fas fa-thermometer-empty', 
                'fa-thermometer-quarter',
                'fa-thermometer-half', 
                'fa-thermometer-three-quarters', 
            ],
            colors: [ 'gray', 'yellow', 'orange', 'red' ],
        }
    },
    computed: {
        color() {
            return this.colors[this.index]
        },
        icon() {
            return this.icons[this.index]
        },
        index() {
            if (this.value < 0 ) return 0
            else if (this.value < 15 ) return 1
            else if (this.value < 30 ) return 2
            else return 3
        },
    }
}
</script>

<style>

</style>