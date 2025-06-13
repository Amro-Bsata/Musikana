<template>
	<div class="song-detail">
		<img :src="song.image_url || 'https://via.placeholder.com/200?text=No+Cover'" alt="Song Cover" class="detail-cover" />
		<div class="detail-info">
			<h3>{{ song.song_name || "Untitled Song" }}</h3>
			<p><strong>Genre:</strong> {{ song.styles?.[0] || "Unknown" }}</p>
			<p v-if="song.owner && context === 'my-songs'"><strong>Owner:</strong> You ({{ song.owner }})</p>
			<p v-if="song.owner && context === 'marketplace'"><strong>Current Owner:</strong> {{ song.owner }}</p>

			<p>
				<em>{{ song.tags || "No additional details available." }}</em>
			</p>

			<div class="audio-player-placeholder">
				<audio ref="audioPlayer" @play="playAudio" @pause="pauseAudio" class="audio-player-hidden" controls v-if="song.audio_url">
					<source :src="song.audio_url" type="audio/mp3" />
					Your browser does not support the audio element.
				</audio>
				<span>Audio Player Placeholder for {{ song.song_name }}</span>
				<button @click="playAudio" v-if="!isAudioPlaying">▶ Play</button>
				<button @click="pauseAudio" v-else>⏸ Pause</button>
			</div>

			<p class="detail-price" v-if="context === 'marketplace' && song.price"><strong>Price:</strong> {{ song.price }}</p>
			<p class="detail-status" v-if="context === 'my-songs' && song.isForSale"><strong>Status:</strong> Listed for sale at {{ song.price }}</p>
			<p class="detail-status" v-if="context === 'my-songs' && !song.isForSale"><strong>Status:</strong> Not currently for sale</p>
		</div>
	</div>
</template>

<script>
export default {
	name: "SongDetail",
	props: {
		song: {
			type: Object,
			required: true,
		},
		context: {
			type: String,
			default: "view", 
		},
	},
	data() {
		return {
			isAudioPlaying: false,
		};
	},
	methods: {
		playAudio() {
			this.$refs.audioPlayer.play();
			this.isAudioPlaying = true;
		},
		pauseAudio() {
			this.$refs.audioPlayer.pause();
			this.isAudioPlaying = false;
		},
	},
};
</script>

<style scoped>
.song-detail {
	display: flex;
	gap: 20px;
	align-items: flex-start;
}

.detail-cover {
	width: 150px;
	height: 150px;
	object-fit: cover;
	border-radius: 8px;
	flex-shrink: 0;
}

.detail-info {
	flex-grow: 1;
}

.detail-info h3 {
	margin-top: 0;
	margin-bottom: 10px;
	font-size: 1.5em;
}

.detail-info p {
	margin: 5px 0;
	line-height: 1.5;
}

.detail-info p em {
	color: #ccc;
	display: block;
	margin-top: 10px;
}

.detail-info .audio-player-placeholder {
	margin-top: 15px;
	padding: 10px;
	background-color: #666;
	border: 1px solid #555;
	border-radius: 5px;
	display: flex;
	justify-content: space-between;
	align-items: center;
	font-size: 0.8em;
	color: #aaa;
}

.detail-info .audio-player-placeholder button {
	padding: 5px 10px;
	cursor: pointer;
	background-color: #777;
	color: #f2f2f2;
	border: none;
	border-radius: 4px;
}
.audio-player-hidden {
	display: none;
}

.detail-price,
.detail-status {
	margin-top: 15px;
	font-weight: bold;
}

.detail-price {
	color: #42b983;
	font-size: 1.2em;
}

.detail-status {
	color: #c1bcbc;
}
</style>
