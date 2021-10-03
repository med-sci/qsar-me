<template>
    <section class="hero">
        <div class="container-fluid">
            <div class="row ">
                <div class="col-12 bg-dark hero-div">
                    <h1 class="display-2 text-light text-center h-2"> Pharmacophore report card 
                        {{ $route.params.id }}
                    </h1>
                </div>
            </div>
        </div>
        <div class="container-md"> 
            <div class="row">
                <div class="col-12" 
                    id="mol-col" 
                    style="height: 400px; width:1000px; position: relative; margin: auto;">
                </div>
                <div class="col-12 py-3">
                    <p>
                    Thank u for using qsar.me! 
                    <br>U could download aligned molecules and pharmacophore data
                    </p>
                </div>
                <div class="row">
                    <div class="col-6">
                        <button class="btn btn-success" >download molecules</button>
                    </div>
                    <div class="col-6">
                        <button class="btn btn-success" >download molecules</button>
                    </div>
            </div>
            </div>
        </div>
    </section>
</template>

<script>
import getPharmacophore from './pharmacophore'
    export default {
        methods:{
        },
        mounted() {
            let recaptchaScript = document.createElement('script')
            recaptchaScript.setAttribute('src', 'https://3Dmol.org/build/3Dmol-min.js')
            document.head.appendChild(recaptchaScript)
            require('./pharmacophore')
            getPharmacophore(this.$route.params.id)
        }
    }
</script>

<style scoped>
.hero-div{
    height: 200px;
}
.ngl{
    height: 250px;
}
</style>