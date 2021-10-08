<template>
  <div class="pa-3">
    <v-row>
      <v-col class="pa-2" cols="4" >
        <div style="border: 10px solid black">
          <p style="font-size:30px">{{new Date() | moment("MM.DD")}}</p>
          <p style="font-size:60px;" class="mb-0">{{new Date() | moment("hh")}}</p>
          <p style="font-size:60px">{{new Date() | moment("mm")}}</p>
        </div>
        <div style="border: 10px solid black">
          날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨<br>날씨
        </div>
        
      </v-col>
      <v-col class="pa-2" cols="8" style="border: 10px solid black">
          앱 배치
          
      </v-col>
    </v-row>
    <div>
    </div>
  </div>
</template>

<script>
  

  export default {
    name: 'Home',

    components: {
      
    },
  }
</script>
