import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import CreateSongPage from '../views/CreateSongPage.vue'
import SongListPage from '../views/SongListPage.vue'
import MarketplacePage from '../views/MarketplacePage.vue'
import MySongsPage from '../views/MySongsPage.vue'
import TopSecretsPage from '../views/TopSecretsPage.vue'
import SongDetails from '../views/SongDetails.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/create',
    name: 'CreateSong',
    component: CreateSongPage
  },
  {
    path: '/songs', 
    name: 'SongList',
    component: SongListPage
  },
  { 
    path: '/songs/:songId',
    name: 'SongDetails',
    component: SongDetails
  },
  {
    path: '/marketplace', 
    name: 'Marketplace',
    component: MarketplacePage
  },
  {
    path: '/my-songs', 
    name: 'MySongs',
    component: MySongsPage

  },
  {
    path: '/top-secrets',
    name: 'TopSecrets',
    component: TopSecretsPage
     
  },

]

const router = createRouter({
  
    history: createWebHistory(), 
    routes
  })



export default router