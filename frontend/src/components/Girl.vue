<template>
  <div>
    <ul v-infinite-scroll="loadMore"
        infinite-scroll-disabled="scrollDisabled"
        infinite-scroll-distance="10"
        class="girl-lazyload-list">
      <li v-for="girl in girls" class="girl-lazyload-item">
        <span>{{ girl.title }}</span>
        <img v-lazy="girl.cover" class="girl-lazyload-image"/>
      </li>
    </ul>
    <p v-show="scrollDisabled && ! allLoaded" class="girl-infinite-loading">
      <mt-spinner type="fading-circle" color="#26a2ff"></mt-spinner>
    </p>
  </div>
</template>

<script>
  export default{
    name: 'girl',
    data () {
      return {
        girls: [],
        scrollDisabled: false,
        page: 1,
        per_page: 10,
        allLoaded: false
      }
    },
    methods: {
      loadMore () {
        console.log('Call loadMore, load page ' + this.page)
        this.scrollDisabled = true
        this.$http.get('/girl', {
          params: {
            page: this.page,
            per_page: this.per_page
          }
        }).then(response => {
          if (response.data.has_next) {
            this.girls = this.girls.concat(response.data.girls)
            this.page += 1
            this.scrollDisabled = false
          } else {
            this.allLoaded = true
          }
        })
      }
    },
    mounted () {
      console.log('Call mounted')
      this.loadMore()
    }

  }
</script>


<style scoped>
  .girl-lazyload-list {
    text-align: center;
    list-style-type: none;
  }
  .girl-lazyload-item {
    width: 300px;
    margin: 0 auto;
    margin-bottom: 10px;
    background-color: #ddd;
  }
  .girl-lazyload-image {
    width: 100%;
    display: block;
  }
  .girl-lazyload-image[lazy=loading] {
    width: 40px;
    height: 300px;
    margin: auto;
  }
</style>
