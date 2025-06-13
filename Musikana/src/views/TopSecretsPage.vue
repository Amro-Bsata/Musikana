<template>
	<div class="top-secrets-page">
	  <h1><LockIcon :size="30" /> Top Secrets Area</h1>
  
		<!-- Nachricht, wenn KEIN Zugriff besteht -->
	   <p v-if="isLoadingSongs" class="loading">
			<LoadingIcon class="icon" :size="40" />
		  </p>
	  <div v-else-if="!hasAccess" class="access-denied">
		<h2><BlockHelperIcon :size="30" /> Access Denied</h2>
		<p>You need a TOP-Fan NFT to access this exclusive content.</p>
		<p>Visit the <router-link to="/marketplace">Marketplace</router-link> to see if any are available!</p>
		<button @click="fetchMySongs" class="retry-button">Check Access Again</button>
	  </div>
  
	  <div v-else class="content-area">
		<div class="song-list">
		  <h3>Exclusive Songs</h3>
		  <p v-if="isLoadingSongs" class="loading">
			<LoadingIcon class="icon" :size="40" />
		  </p>
		  <p v-else-if="songsList.length === 0">No exclusive songs found.</p>
		  <SongCard
			v-else
			v-for="song in songsList"
			:key="song.id"
			:song="song"
			@click="selectSong(song)"
			:class="{ selected: selectedSong && selectedSong.id === song.id }"
		  />
		</div>
  
		<!-- Rechte Seite: Song Detail & Tabs (wird nur angezeigt, wenn ein Song ausgewählt ist) -->
		<div class="song-detail-view" v-if="selectedSong">
		  <h2>Details for: {{ selectedSong.song_name }}</h2>
		  <div class="detail-summary">
			   <img :src="selectedSong.image_url || 'https://placehold.co/150?text=No+Cover'" alt="Song Cover" class="detail-cover">
			   <div class="detail-info">
				  <h3>{{ selectedSong.song_name || 'Untitled Song' }}</h3>
				  <p><strong>Genre:</strong> {{ selectedSong.styles?.[0] || 'Unknown' }}</p>
				  <p v-if="selectedSong.artist"><strong>Artist:</strong> {{ selectedSong.artist }}</p>
				  <div class="audio-player-placeholder">
					<audio ref="audioPlayer" @play="playAudio" @pause="pauseAudio" class="audio-player-hidden" controls v-if="selectedSong.audio_url">
					  <source :src="selectedSong.audio_url" type="audio/mp3" />
					  Your browser does not support the audio element.
					</audio>
					<span>Audio Player Placeholder for {{ selectedSong.song_name }}</span>
					<button @click="playAudio" v-if="!isAudioPlaying">▶ Play</button>
					<button @click="pauseAudio" v-else>⏸ Pause</button>
				  </div>
			   </div>
		  </div>
  
		  <div class="content-wrapper-tabs">
			  <div class="tabs">
				<button @click="activeTab = 'channel'" :class="{ active: activeTab === 'channel' }">
				   <BroadcastIcon :size="20" /> Channel
				</button>
				<button @click="activeTab = 'mv'" :class="{ active: activeTab === 'mv' }">
				   <VideoIcon :size="20" /> MV
				</button>
				<button @click="activeTab = 'remixes'" :class="{ active: activeTab === 'remixes' }">
				   <AlbumIcon :size="20" /> Remixes
				</button>
			  </div>
  
			  <div class="tab-content">
				<div v-if="activeTab === 'channel'">
				  <h2>Exclusive Channel Content</h2>
				  <p>Behind-the-scenes, special announcements, etc.</p>
				  <p v-if="selectedSong.chat.length > 0">{{ selectedSong.chat?.[0]?.message }}</p>
				  <div v-else class="content-placeholder">Channel Area for {{ selectedSong.song_name }}</div>
				</div>
				<div v-if="activeTab === 'mv'">
				  <h2>Official Music Video</h2>
				  <p>Watch the exclusive official music video here.</p>
				   <p v-if="selectedSong.mv">{{ selectedSong.mv }}</p>
				  <div v-else class="content-placeholder video">MV Area (Video Player Placeholder) for {{ selectedSong.song_name }}</div>
				</div>
				<div v-if="activeTab === 'remixes'">
				  <h2>Exclusive Remixes</h2>
				  <p>Listen to or download special remixes.</p>
				  <ul v-if="selectedSong.remixs.length > 0" v-for="remix in selectedSong.remixs" :key="remix.id">
					<a :href="remix.url" target="_blank"><li>{{ remix.title }}</li></a>
				  </ul>
				  <div v-else class="content-placeholder audio-list">Remix 1, Remix 2... for {{ selectedSong.song_name }}</div>
				</div>
			  </div>
		  </div>
  
		</div>
		<div class="song-detail-view placeholder" v-else>
		  <p>Select a song from the list to view exclusive content.</p>
		</div>
	  </div>
	</div>
  </template>

<script>
import { ref, onMounted } from "vue";
import LockIcon from "vue-material-design-icons/Lock.vue";
import BlockHelperIcon from "vue-material-design-icons/BlockHelper.vue";
import BroadcastIcon from "vue-material-design-icons/Broadcast.vue";
import VideoIcon from "vue-material-design-icons/Video.vue";
import AlbumIcon from "vue-material-design-icons/Album.vue";
import LoadingIcon from "vue-material-design-icons/Loading.vue";
import SongCard from "@/components/SongCard.vue";
import Cookies from "js-cookie";
import { ethers } from "ethers";
import axios from "axios";
import { API_URL } from "@/utils";

export default {
	name: "TopSecretsPage",
	components: {
		LockIcon,
		BlockHelperIcon,
		BroadcastIcon,
		VideoIcon,
		AlbumIcon,
		LoadingIcon,
		SongCard,
	},
	setup() {
		const hasAccess = ref(false);
		const isLoadingSongs = ref(false);
		const songsList = ref([]);
		const selectedSong = ref(null);
		const activeTab = ref("channel");
		const audioPlayer = ref(null);
		const isAudioPlaying = ref(false);
		const isLoadingSongDetails = ref(false);
		const token = ref(Cookies.get("access_token"));

		async function checkWalletConnection() {
			let walletAddress = Cookies.get("address");
			if (!walletAddress) {
				const provider = new ethers.providers.Web3Provider(window.ethereum);
				await provider.send("eth_requestAccounts", []);
				const signer = provider.getSigner();
				const address = await signer.getAddress();
				Cookies.set("address", address, { expires: 1 });
				walletAddress = address;
			}
			return walletAddress;
		}
		async function fetchMySongs() {
			const walletAddress = await checkWalletConnection();
			if (!walletAddress) return;

			isLoadingSongs.value = true;
			try {
				const response = await axios.get(`${API_URL}wallet/${walletAddress}`);

				const songsWithImages = await Promise.all(
					response.data.FAN_NFT.map(async (song) => {
						let image = null;

						try {
							if (song.uri) {
								const meta = await axios.get(song.uri);
								image = meta?.data?.response?.data?.data?.[0]?.image_url || null;
							}
						} catch (err) {
							console.warn(`Failed to fetch image for song ${song.song_name}`, err);
						}

						return {
							id: song.song_id,
							song_name: song.song_name,
							styles: song.styles || "Unknown",
							price: (song.copyright_nft_price / 1000000000).toFixed(8),
							nftId: song.song_id,
							nftContract: song.copyright_nft_contract,
							nftLink: song.uri,
							nftType: "Fan-NFT",
							owner: song.owner,
							owner_nft_contract: song.owner_nft_contract,
							url: song.uri,
							image_url: image,
						};
					}),
				);

				if (songsWithImages.length === 0) {
					hasAccess.value = false;
					return;
				}
				hasAccess.value = true;
				isLoadingSongs.value = false;
				songsList.value = songsWithImages;
			} catch (error) {
				console.error("Error fetching songs:", error);
			} finally {
				isLoadingSongs.value = false;
			}
		}
		async function fetchSongDetails(song) {
			if (!song.url) return;

			try {
				isLoadingSongDetails.value = true;
				const response = await axios.get(song.url);
				const fanArea = await axios.get(`${API_URL}get/fan/area/${song.id}`, {
					headers: {
						Authorization: `Bearer ${token.value}`,
					},
				});
				const areaData = fanArea.data;
				const apiResponse = response?.data?.response?.data?.data?.[0];
				const songData = {
					...song,
					...areaData,
					...(apiResponse || {}),
				};
				selectedSong.value = songData;
			} catch (error) {
				console.error("Error fetching song details:", error);
			} finally {
				isLoadingSongDetails.value = false;
			}
		}

		async function selectSong(song) {
			await fetchSongDetails(song);
			activeTab.value = "channel";
		}

		function playAudio() {
			audioPlayer.value.play();
			isAudioPlaying.value = true;
		}

		function pauseAudio() {
			audioPlayer.value.pause();
			isAudioPlaying.value = false;
		}

		onMounted(() => {
			fetchMySongs();
		});

		return {
			hasAccess,
			isLoadingSongs,
			songsList,
			selectedSong,
			activeTab,
			fetchMySongs,
			selectSong,
			audioPlayer,
			isAudioPlaying,
			playAudio,
			pauseAudio,
			isLoadingSongDetails,
		};
	},
};
</script>

<style scoped>

.top-secrets-page {
  max-width: 1200px; 
  margin: 20px auto;
  padding: 20px; 
  background-color: var(--color-background); 
  color: var(--color-text);
}

.top-secrets-page h1 {

  color: var(--color-primary);
  border-bottom: 1px solid var(--color-primary-hover); 
  padding-bottom: 10px;
  margin-bottom: 20px;
  display: flex; 
  align-items: center; 
  gap: 10px; 
}

.top-secrets-page > p {
 
  color: #ff6b6b; 
  font-weight: bold;
  text-align: center;
  padding: 20px;
  border: 1px solid #444; 
  background-color: #555;
  border-radius: 5px;
  margin-top: 20px; 
}


.content-area {
  display: flex;
  gap: 30px; 
  min-height: 500px; 
}

.song-detail-view h2 {
    color: var(--color-primary-hover);
}

.content-wrapper-tabs {
    border-radius: 8px; 
    overflow: hidden;
}

.waveform-placeholder {
  padding: 0 15px;
  font-size: 1.5em;
  color: #aaa; 
  padding: 10px 0;
  background-color: #f5f5f5; 
  border-bottom: 1px solid #eee; 
  flex-shrink: 0;
  color: #aaa; 
  background-color: #f5f5f5; 
  border-bottom: 1px solid #eee; 
}

.tab-content h2 {
    color: #f2f2f2; 
    margin-top: 0;
    margin-bottom: 15px;
}
.tab-content p {
    margin-bottom: 15px;
}


.content-area-tab > div {
    margin-top: 20px; 
    border: 1px dashed #ccc; 
    display: flex;
    justify-content: center;
    align-items: center;
    color: #aaa;
    border-radius: 4px;
    font-style: italic;
}
.content-area-tab .channel-post {
   background-color: #666;
   border: none; 
   border-left: 3px solid #42b983; 
   padding: 15px;
   margin-bottom: 15px;
   color: #f2f2f2;
   display: block; 
   text-align: left;
}
.content-area-tab .channel-post h4 {
   color: #f2f2f2;
   margin-top: 0;
   margin-bottom: 5px;
}
.content-area-tab .channel-post p {
    margin-bottom: 5px;
    color: #ccc;
}
.content-area-tab .channel-post small {
    color: #aaa;
    font-style: italic;
}


.content-placeholder {
  min-height: 200px;
  background-color: #555;
  border: 1px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #aaa; 
  margin-top: 20px;
  border-radius: 4px;
  font-style: italic;
}

.content-placeholder.video {
  background-color: #333;
}

.content-placeholder.audio-list {
  background-color: #777;
}

@media (max-width: 768px) {
  .content-area {
    flex-direction: column; 
    gap: 20px; 
  }

  .song-list {
    max-width: 100%; 
    overflow-y: visible; 
    max-height: none;
  }

  .song-detail-view {
    flex: auto; 
  }
   .detail-summary {
       flex-direction: column; 
       align-items: center; 
       text-align: center;
   }
   .detail-summary .detail-info p {
       text-align: left; 
   }
   .tabs button {
       padding: 10px 15px; 
       font-size: 0.9em;
   }
    .tabs button:first-of-type {
       margin-left: 40px; 
   }
   .tabs .extra-button {
        left: 5px;
   }
}

</style>
