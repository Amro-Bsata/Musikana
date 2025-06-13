<template>
	<div class="song-list-page">
		<div class="header-box">
			<h1>All Songs</h1>
			<router-link to="/create" class="cta-button">Create Song</router-link>
		</div>

		<div class="filters">
			<label for="genre-filter">Filter by Genre:</label>
			<select id="genre-filter" v-model="selectedGenre" @change="filterSongs">
				<option value="">All Genres</option>
				<option v-for="genre in genres" :key="genre.value" :value="genre.value">{{ genre.label }}</option>
			</select>
		</div>

		<div :class="{ 'song-grid': !loading }">
			<p v-if="loading" class="loading">
				<BxLoaderCircle class="icon" />
			</p>
			<p v-else-if="displayedSongs.length === 0">No songs found{{ selectedGenre ? " for genre " + selectedGenre : "" }}.</p>
			<SongCard v-else v-for="song in displayedSongs" :key="song.song_id" :song="song" @click="viewSongDetail(song.song_id)" />
		</div>

		<div class="pagination" v-if="filteredSongList.length > songsPerPage">
			<button @click="loadMore" :disabled="!canLoadMore">
				{{ canLoadMore ? "Load More" : "No More Songs" }}
			</button>
		</div>
		<p class="debug-info">Showing {{ displayedSongs.length }} of {{ filteredSongList.length }} songs.</p>
	</div>
</template>

<script>
import axios from "axios";
import SongCard from "@/components/SongCard.vue"; 
import { GENRES, API_URL } from "@/utils";
import { BxLoaderCircle } from "@kalimahapps/vue-icons";

export default {
	name: "SongListPage",
	components: {
		SongCard,
		BxLoaderCircle,
	},
	data() {
		return {
			loading: false,
			allSongs: [], // Alle verfügbaren Songs vom Backend
			selectedGenre: "",
			currentPage: 1,
			songsPerPage: 9, // Wieviele Songs pro "Seite" oder pro Klick auf "Load More"
			genres: GENRES,
		};
	},
	computed: {
		filteredSongList() {
			if (!this.selectedGenre) {
				return this.allSongs;
			}
			return this.allSongs.filter((song) => song.styles.includes(this.selectedGenre));
		},
		displayedSongs() {
			const end = this.currentPage * this.songsPerPage;
			return this.filteredSongList.slice(0, end);
		},
		canLoadMore() {
			return this.displayedSongs.length < this.filteredSongList.length;
		},
	},
	methods: {
		async fetchAllSongs() {
			this.loading = true;
			try {
				const response = await axios.get(`${API_URL}songs/?firstID=${this.currentPage}&lastID=${(this.currentPage + 1) * this.songsPerPage}`);

				const songsWithImages = await Promise.all(
					response.data.map(async (song) => {
						let image = null;

						try {
							if (song.uri) {
								const meta = await axios.get(song.uri);
								image = meta?.data?.response?.data?.data?.[0]?.image_url || null;
							}
						} catch (err) {
							console.warn(`Couldn't fetch image for song ${song.song_name}`, err);
						}

						return {
							...song,
							price: (song.copyright_nft_price / 1000000000).toFixed(8),
							image_url: image,
						};
					}),
				);

				this.allSongs = songsWithImages;
			} catch (error) {
				console.error("Error fetching songs:", error);
				this.allSongs = [];
			} finally {
				this.loading = false;
			}
		},

		filterSongs() {
			// Wenn Filter geändert wird, Paginierung zurücksetzen
			this.currentPage = 1;
			
		},
		viewSongDetail(songId) {
			this.$router.push({ name: "SongDetails", params: { songId } });
		},
		loadMore() {
			if (this.canLoadMore) {
				this.currentPage++;
				this.fetchAllSongs();
			}
		},
	},
	created() {
		this.fetchAllSongs(); // Lade alle Songs beim Erstellen
	},
};
</script>

<style scoped>
.header-box {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 4px;
	flex-wrap: wrap;
	padding-bottom: 10px;
}

.song-list-page {
	max-width: 1200px;
	margin: auto;
	padding-bottom: 50px;
}

.filters {
	margin-bottom: 25px;
	padding: 15px;
	background-color: #555;
	border-radius: 8px;
}

.filters label {
	margin-right: 10px;
	font-weight: bold;
}

.filters select {
	padding: 8px 12px;
	border: 1px solid #ccc;
	border-radius: 4px;
}

.song-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 20px;
	margin-bottom: 30px;
}

.pagination {
	text-align: center;
	margin-top: 20px;
}

.pagination button {
	padding: 10px 25px;
	background-color: #42b983;
	color: white;
	border: none;
	border-radius: 5px;
	cursor: pointer;
	font-size: 1em;
}

.pagination button:disabled {
	background-color: #ccc;
	cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
	background-color: #36a86e;
}

.debug-info {
	text-align: center;
	margin-top: 10px;
	color: #888;
	font-size: 0.9em;
	font-style: italic;
}
</style>
