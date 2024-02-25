<script>
export default {
    name: 'FavoriteView'
}
</script>

<template>
    <div>
        <img src="https://cdn-icons-png.flaticon.com/512/5229/5229377.png"/>
    </div>
</template>

<style scoped>
    div {
        box-sizing: border-box;
        width: auto;
        height: 80vh;
        background-color: #ececec;
        margin: 0 30px;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    body.dark-mode div {
        background-color: #373737;
    }
    img {
        width: 100px;
    }
</style>