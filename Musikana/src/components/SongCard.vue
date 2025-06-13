<template>
	<div class="song-card">
		<img :src="song.image_url || 'https://placehold.co/100?text=No+Cover'" alt="Song Cover" class="song-cover" />
		<div class="song-info">
			<h4 class="song-name">{{ song.song_name || "Untitled Song" }}</h4>
			<p class="song-genre">{{ song.styles?.[0] || "Unknown Genre" }}</p>
			<p class="song-details" v-if="song.details">{{ song.details }}</p>
			<p class="song-price" v-if="song.price">{{ song.price }}</p>
		</div>
	</div>
</template>

<script>
export default {
	name: "SongCard",
	props: {
		song: {
			type: Object,
			required: true,
		},
	},
};
</script>

<style scoped>
.song-cover {
	width: 60px;
	height: 60px;
	object-fit: cover;
	border-radius: 4px;
	flex-shrink: 0;
}

.song-info {
	flex-grow: 1;
	overflow: hidden;
}

.song-name {
	margin: 0 0 5px 0;
	font-size: 1.1em;
	font-weight: 500;
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	color: var(--color-primary);
}

.song-genre,
.song-details,
.song-price {
	margin: 2px 0;
	font-size: 0.9em;
	color: var(--color-primary);
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.song-price {
	font-weight: bold;
	color: var(--color-primary);
}
</style>
