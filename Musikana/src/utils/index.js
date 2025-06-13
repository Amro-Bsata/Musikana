export const CUSTOM_URL = "https://sepolia.etherscan.io/";
export const API_URL = "http://127.0.0.1:5001/";
export const ADDRESS = "0xC66e27C667Afa77cc134A34D589de37a58e2b9FE";
export const INFURA_URL = "https://sepolia.infura.io/v3/2b731abb6acd4158b7642d8e38d7f512";
export const ABI = [
	{
		inputs: [
			{
				internalType: "address",
				name: "new_owner",
				type: "address",
			},
		],
		name: "transferOwnership",
		outputs: [],
		stateMutability: "nonpayable",
		type: "function",
	},
];

export const GENRES = [
	{ value: "Pop", label: "Pop" },
	{ value: "Rock", label: "Rock" },
	{ value: "Synthwave", label: "Synthwave" },
	{ value: "Classical", label: "Classical" },
	{ value: "Hip Hop", label: "Hip Hop" },
	{ value: "Lo-Fi", label: "Lo-Fi" },
	{ value: "Rap", label: "Rap" },
	{ value: "R&B", label: "R&B" },
	{ value: "Electronic", label: "Electronic" },
	{ value: "Jazz", label: "Jazz" },
	{ value: "Country", label: "Country" },
	{ value: "Indie", label: "Indie" },
	{ value: "Metal", label: "Metal" },
	{ value: "Reggae", label: "Reggae" },
	{ value: "Techno", label: "Techno" },
	{ value: "Trance", label: "Trance" },
	{ value: "Trip-Hop", label: "Trip-Hop" },
	{ value: "Vaporwave", label: "Vaporwave" },
	{ value: "World", label: "World" },
];


export const songsContractABI = [
	{
		inputs: [
			{
				internalType: "string",
				name: "song_name",
				type: "string",
			},
			{
				internalType: "string[]",
				name: "styles",
				type: "string[]",
			},
			{
				internalType: "string[]",
				name: "negativ_styels",
				type: "string[]",
			},
			{
				internalType: "string",
				name: "uri",
				type: "string",
			},
			{
				internalType: "uint32",
				name: "fan_nft_maxSupply",
				type: "uint32",
			},
			{
				internalType: "uint32",
				name: "copyright_nft_maxSupply",
				type: "uint32",
			},
			{
				internalType: "uint256",
				name: "copyright_nft_price",
				type: "uint256",
			},
		],
		name: "create_song",
		outputs: [
			{
				internalType: "uint32",
				name: "",
				type: "uint32",
			},
		],
		stateMutability: "nonpayable",
		type: "function",
	},
	{
		inputs: [
			{
				internalType: "uint32",
				name: "song_id",
				type: "uint32",
			},
			{
				internalType: "address",
				name: "owner_address",
				type: "address",
			},
		],
		name: "newOwner",
		outputs: [],
		stateMutability: "nonpayable",
		type: "function",
	},
	{
		inputs: [],
		stateMutability: "nonpayable",
		type: "constructor",
	},
	{
		inputs: [
			{
				internalType: "string",
				name: "",
				type: "string",
			},
			{
				internalType: "uint256",
				name: "",
				type: "uint256",
			},
		],
		name: "genreToSongIds",
		outputs: [
			{
				internalType: "uint32",
				name: "",
				type: "uint32",
			},
		],
		stateMutability: "view",
		type: "function",
	},
	{
		inputs: [
			{
				internalType: "uint32",
				name: "song_id",
				type: "uint32",
			},
		],
		name: "get_song",
		outputs: [
			{
				components: [
					{
						internalType: "uint32",
						name: "song_id",
						type: "uint32",
					},
					{
						internalType: "string",
						name: "song_name",
						type: "string",
					},
					{
						internalType: "string[]",
						name: "styles",
						type: "string[]",
					},
					{
						internalType: "string[]",
						name: "negativ_styels",
						type: "string[]",
					},
					{
						internalType: "string",
						name: "uri",
						type: "string",
					},
					{
						internalType: "uint32",
						name: "fan_nft_maxSupply",
						type: "uint32",
					},
					{
						internalType: "uint32",
						name: "copyright_nft_maxSupply",
						type: "uint32",
					},
					{
						internalType: "uint256",
						name: "copyright_nft_price",
						type: "uint256",
					},
					{
						internalType: "address",
						name: "owner_nft_contract",
						type: "address",
					},
					{
						internalType: "address",
						name: "fan_nft_contract",
						type: "address",
					},
					{
						internalType: "address",
						name: "copyright_nft_contract",
						type: "address",
					},
					{
						internalType: "address",
						name: "owner",
						type: "address",
					},
				],
				internalType: "struct Songs.song",
				name: "",
				type: "tuple",
			},
		],
		stateMutability: "view",
		type: "function",
	},
	{
		inputs: [
			{
				internalType: "string",
				name: "genre",
				type: "string",
			},
		],
		name: "get_songs_by_genre",
		outputs: [
			{
				internalType: "uint32[]",
				name: "",
				type: "uint32[]",
			},
		],
		stateMutability: "view",
		type: "function",
	},
	{
		inputs: [],
		name: "next_song_id",
		outputs: [
			{
				internalType: "uint32",
				name: "",
				type: "uint32",
			},
		],
		stateMutability: "view",
		type: "function",
	},
	{
		inputs: [
			{
				internalType: "uint32",
				name: "",
				type: "uint32",
			},
		],
		name: "songs",
		outputs: [
			{
				internalType: "uint32",
				name: "song_id",
				type: "uint32",
			},
			{
				internalType: "string",
				name: "song_name",
				type: "string",
			},
			{
				internalType: "string",
				name: "uri",
				type: "string",
			},
			{
				internalType: "uint32",
				name: "fan_nft_maxSupply",
				type: "uint32",
			},
			{
				internalType: "uint32",
				name: "copyright_nft_maxSupply",
				type: "uint32",
			},
			{
				internalType: "uint256",
				name: "copyright_nft_price",
				type: "uint256",
			},
			{
				internalType: "address",
				name: "owner_nft_contract",
				type: "address",
			},
			{
				internalType: "address",
				name: "fan_nft_contract",
				type: "address",
			},
			{
				internalType: "address",
				name: "copyright_nft_contract",
				type: "address",
			},
			{
				internalType: "address",
				name: "owner",
				type: "address",
			},
		],
		stateMutability: "view",
		type: "function",
	},
];



	export const copyrightNFTContractABI = [          // ABI NUR für 'mintToken'-Funktion
		{
		inputs: [],
		name: "price",
		outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
		stateMutability: "view",
		type: "function",
		},
		{
		inputs: [{ internalType: "address", name: "_to", type: "address" }],
		name: "mintToken",
		outputs: [],
		stateMutability: "payable",
		type: "function",
		},
	];