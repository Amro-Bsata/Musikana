<template>
  <div id="app">
    <nav class="main-nav">
      <div class="logo">Musikana</div>
      <div class="MetaMaskLogin">
        <MetaMaskLogin />
      </div>
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/songs">Songs</router-link>
        <router-link to="/marketplace">Marketplace</router-link>
        <router-link to="/top-secrets">Top Secrets</router-link>
      </div>
      <div class="user-actions">
        <router-link to="/my-songs">My Songs</router-link>
        <span class="profile-icon">👤</span>
      </div>
    </nav>
    <main>
      <router-view />
      <!-- VUEE APP -->
    </main>
  </div>
</template>

<script>
import MetaMaskLogin from './components/MetaMaskLogin.vue';


export default {
  name: "App",
  components: {
    MetaMaskLogin
  }
};



</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #42b983;
}

.main-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #555;
  border-bottom: 1px solid #444;
  margin-bottom: 20px;
  /* Platz vor dem Inhalt */
}

.logo {
  font-weight: bold;
  font-size: 1.5em;
  text-shadow: 0px 1px 6px #42b983;
}

.nav-links a {
  margin: 0 10px;
  text-decoration: none;
  color: #42b983;
  font-weight: bold;
}

.nav-links a.router-link-exact-active {
  color: #42b983;
  border-bottom: 2px solid #42b983;
}

.user-actions {
  display: flex;
  align-items: center;
}

.user-actions a {
  margin-right: 15px;
  text-decoration: none;
  color: #42b983;
  font-weight: bold;
}

.profile-icon {
  font-size: 1.5em;
  cursor: pointer;
  
}

main {
  padding: 0 20px;
  
}

.MetaMaskLogin {
  display: flex;
  gap: 10px;
}
</style>
