<template>
	<div class="home-page-wrapper">
		<main class="main-content">
			<section id="hero-cta" class="hero-section">
				<h2 class="animate-fade-in-down">Welcome to the AI Music Platform!</h2>
				<p class="animate-fade-in-up delay-1">
					Unleash your creativity and compose unique musical pieces with the power of artificial intelligence – no prior experience needed.
				</p>

				<!-- CTA BOXX -->
				<div class="cta-box animate-fade-in-up delay-2">
					<h3>Electric Your First Song!</h3>
					<p>Generate unique music with AI in minutes.</p>
					<router-link to="/create" class="cta-button">Create Now</router-link>
				</div>
			</section>

			<!-- HOW IT WORKS SECTION -->
			<section id="how-it-works" ref="howItWorksSection" class="content-section feature-overview">
				<h3>How It Works</h3>
				<div class="steps-container">
					<div class="step">
						<div class="step-icon">🎨</div>
						<h4>1. Choose Your Style</h4>
						<p>Select from genres, moods, or instruments.</p>
					</div>
					<div class="step">
						<div class="step-icon">⚙️</div>
						<h4>2. Define Parameters</h4>
						<p>Set tempo, key, or complexity.</p>
					</div>
					<div class="step">
						<div class="step-icon">✨</div>
						<h4>3. AI Composes</h4>
						<p>Our AI creates your unique piece of music.</p>
					</div>
					<div class="step">
						<div class="step-icon">💎</div>
						<h4>4. Create NFT</h4>
						<p>Your song is registered with us, and (OWNER, NFT, COpyRIght) NFTs are created for it.</p>
					</div>
					<div class="step">
						<div class="step-icon">💾</div>
						<h4>5. Download & Use</h4>
						<p>Your song, ready for your projects.</p>
					</div>
				</div>
			</section>


			<!-- Feedback -->
			<section id="testimonials" ref="testimonialsSection" class="content-section testimonials">
				<h3>What our users say</h3>
				<div class="testimonial-grid">
					<div class="testimonial-item">
						<p>"Diese Plattform hat meine Content-Erstellung revolutioniert! So schnell und einfach tolle Musik."</p>
						<h4>- Kevin SchwaCHz, Moviestar</h4>
					</div>
					<div class="testimonial-item">
						<p>"ich schwöre, Bruder! Diese Plattform ist übel krank! Mashallah, so einfach, selbst mein Esel könnte damit Chart-Hits machen!"</p>
						<h4>- ABU, kein Job</h4>
					</div>
					<div class="testimonial-item">
						<p>"Nicht schlecht"</p>
						<h4>- Felix , Software Tester</h4>
					</div>
				</div>
			</section>
		</main>
		<footer class="page-footer">
			<p>© {{ new Date().getFullYear() }} MusikApp. All rights reserved.</p>
		</footer>
	</div>
</template>

<script>
export default {
	name: "HomePage",
	mounted() {
		this.observeSections();
	},
	beforeUnmount() {
		if (this.observer) {
			this.observer.disconnect();
		}
	},
	methods: {
		observeSections() {
			const options = {
				root: null,
				rootMargin: "0px",
				threshold: 0.1,
			};

			this.observer = new IntersectionObserver((entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						entry.target.classList.add("is-visible");
					}
				});
			}, options);

			// Observe jede section , observer pattern :)
			const sectionsToObserve = [
				this.$refs.howItWorksSection,
				this.$refs.testimonialsSection,
			];
			sectionsToObserve.forEach(section => {
				if (section) this.observer.observe(section);
			});
		},
		scrollToSection(sectionId) {
			const element = document.getElementById(sectionId);
			if (element) {
				element.scrollIntoView({ behavior: "smooth", block: "start" });
			}
		},
	},
};
</script>

<style scoped>
/* General page layout */
.home-page-wrapper {
	display: flex;
	flex-direction: column;
	min-height: 100vh; /* wichtig damit, dass der Footer unten ist, wenn der Inhalt kurz ist */
}


.main-content {
	flex-grow: 1;
    padding: 20px; 
	max-width: 1200px;
	margin: 0 auto; /* zentrieren */
}

/* Hero Section */
.hero-section {
    margin-bottom: 50px;
}

.main-content h2 { /* Hauptüberschrift der Seite */
	font-size: 2.5em;
	color: #e0e0e0;
	margin-bottom: 15px;
}

.main-content > .hero-section > p { /*  Intro-Absatz */
	font-size: 1.1em;
	color: #b0b0b0;
	line-height: 1.6;
	margin-bottom: 30px;
}

/* CTA Box Styling */
.cta-box {
	border: none;
	padding: 30px 25px;
	text-align: center;
	background-color: #3a3a3a;
	border-radius: 12px;
	margin-top: 20px;
	margin-bottom: 50px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 15px;
	box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.cta-box h3 {
	font-size: 1.8em;
	color: #42b983;
	margin: 0;
}

.cta-box p {
	font-size: 1em;
	color: #c0c0c0;
	margin: 0;
}

.cta-button {
	background-color: #42b983;
	color: white;
	padding: 12px 30px;
	text-decoration: none;
	border-radius: 25px;
	font-weight: bold;
	font-size: 1.1em;
	transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
	box-shadow: 0 4px 10px rgba(66, 185, 131, 0.4);
}

.cta-button:hover {
	background-color: #36a372;
	transform: translateY(-2px) scale(1.02);
	box-shadow: 0 6px 15px rgba(66, 185, 131, 0.5);
}

/* Content Sections Styling */
.content-section {
	margin-bottom: 70px;
	padding-top: 30px;
	opacity: 0;
	transform: translateY(30px);
	transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    scroll-margin-top: 20px;
}

.content-section.is-visible {
	opacity: 1;
	transform: translateY(0);
}

.content-section > h3 { /* Section main heading */
	font-size: 1.8em;
	color: #42b983;
	margin-bottom: 25px;
	border-bottom: 1px solid #555;
	padding-bottom: 15px;
	text-align: center;
}



.content-section p,
.content-section ul {
	font-size: 1em;
	color: #b0b0b0;
	line-height: 1.7;
	margin-bottom: 15px;
}

.content-section ul {
	list-style: disc;
	padding-left: 25px;
}

.content-section ul li {
	margin-bottom: 8px;
}


/* How it Works Section */
.feature-overview h3 {
	margin-bottom: 40px;
}
.steps-container {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
	gap: 25px;
}
.step {
	background-color: #2a2a2a;
	padding: 25px 20px;
	border-radius: 8px;
	text-align: left;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.step:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}
.step-icon {
	font-size: 2.8em;
	margin-bottom: 20px;
	color: #42b983;
    display: block;
    text-align: center;
}
.step h4 {
	font-size: 1.1em;
	color: #d0d0d0;
	margin-bottom: 10px;
    text-align: center;
}
.step p {
    font-size: 0.95em;
    color: #a0a0a0;
    text-align: center;
}

/* Testimonials Section */
.testimonials h3 { 
    margin-bottom: 40px;
}
.testimonial-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	gap: 25px;
}
.testimonial-item {
	background-color: #2a2a2a;
	padding: 25px;
	border-radius: 8px;
	border-left: 4px solid #42b983;
	box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.testimonial-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
}
.testimonial-item p { 
	font-style: italic;
	color: #b0b0b0;
	margin-bottom: 15px;
	position: relative;
}
.testimonial-item h4 { 
	font-size: 0.9em;
	color: #888;
	text-align: right;
}


/* Footer */
.page-footer {
	background-color: #1c1c1c;
	color: #777;
	text-align: center;
	padding: 25px 20px;
	margin-top: auto;
	border-top: 1px solid #333;
}
.page-footer p {
	margin: 0;
	font-size: 0.9em;
}


/* Animationen */
@keyframes fadeInDown {
	from { opacity: 0; transform: translateY(-20px); }
	to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp {
	from { opacity: 0; transform: translateY(20px); }
	to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-down { animation: fadeInDown 0.7s ease-out forwards; }
.animate-fade-in-up { opacity: 0; animation: fadeInUp 0.7s ease-out forwards; }

.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }
.delay-3 { animation-delay: 0.6s; }
</style>