const { createApp } = Vue

const CluelessApp = {
	data() {
		return {
			s: '',
			solution: []
		}
	},
	async created(){
		await this.getSolution()
	},
	methods: {
		async getSolution(){
			const response = await fetch(window.location, {
				method: 'get',
				headers: {
					'X-Requested-With': 'XMLHttpRequest'
				}
			})

			this.solution = await response.json()

			console.log(this.solution)
		}
	},
	delimiters: ['{', '}']
}

createApp(CluelessApp).mount('#app')