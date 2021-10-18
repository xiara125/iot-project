<template>
    <div class="text-center">
        <!-- <v-icon x-large class="mr-3 float-left" 
            :color="color">mdi-brightness-7</v-icon> -->
        <div  class="font-weight-bold">조도</div>
        <span>{{value}}lx</span>
    </div>

</template>

<script>
export default {
    name: 'Illusion',
    props: ['value'],
    data(){
        return {
            colors: ['grey darken-4', 'grey darken-2', 
               'yellow accent-1', 'yellow accent-2', 'yellow accent-4']

        }
    },
    computed:{
        color(){
            return this.colors[this.index]
        },
        index(){
            return parseInt(this.value/20)
        }
    }
}
</script>

<style>

</style>