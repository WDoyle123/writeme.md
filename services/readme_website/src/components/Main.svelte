<script>
	import Step from './Step.svelte';
	let steps = [
		{ name: 'Autogen', icon: 'fa-solid fa-robot' },
		{ name: 'Docker & Kubernetes', icon: 'fa-brands fa-docker' },
		{ name: 'Terraform', icon: 'fa-solid fa-cloud' }
	];

	let benefits = [
		{
			metric: 'Frontend',
			name: 'Getting the user input',
			description:
				'We begin by getting the user email and repository that the user has requested writeme to make a readme.md file on. This is then passed to the backend using an API call.'
		},
		{
			metric: 'Backend',
			name: 'Processing the data',
			description:
				'The repository is cloned and the data is then passed to the AI agents where they begin the analysis. The end result is a readme.md file genereted by the llm workers and subsequently emailed to the end user.'
		},
		{
			metric: 'Deployment',
			name: 'Running the service',
			description:
				'To host the service we ustilise Docker, Kubernetes and Terraform to use cloud computing services.'
		}
	];

	let email = '';
	let repositoryName = '';
  let openaiApiKey = '';
  let openaiModel = '';
	let message = '';
	let isLoading = false;

  const API_BASE_URL = 'http://writeme.com/api';

	async function handleSubmit() {
		isLoading = true;
		message = '';

		if (!email || !repositoryName || !openaiApiKey || !openaiModel) {
			console.error('Submission failed: cannot be empty.');
			message = 'Submission failed: cannot be empty.';
			return;
		}

		console.log('email:', email, 'repository name:', repositoryName);
		console.debug('Preparing to send request to', `${API_BASE_URL}/upload`);

		try {
			console.debug('Preparing to send request to', `${API_BASE_URL}/upload`);
			const requestDetails = {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email, repositoryName, openaiApiKey, openaiModel })
			};
			console.debug('Request details:', JSON.stringify(requestDetails, null, 2));

			const response = await fetch(`${API_BASE_URL}/upload`, requestDetails);

			console.log('Response received with status:', response.status);
			console.debug(
				'Response headers:',
				JSON.stringify(Object.fromEntries(response.headers.entries()))
			);

			if (response.ok) {
				const responseData = await response.json();
				message = responseData.message;
				console.log('Success response:', message);
			} else {
				const errorData = await response.json();
				message = `Submission failed: ${errorData.error}`;
				console.log('Failed with error:', message);
				console.debug('Error response details:', JSON.stringify(errorData));
			}
		} catch (error) {
			message = `Network error: ${error.message}`;
			console.error('Network or other error:', error);
			console.debug('Error details:', error);
		} finally {
      setTimeout(() => {
        console.log("Waited 5 seconds");
      }, 5000); 
			isLoading = false;
			console.log('Done with submission process.');
		}
	}
</script>

<main class="flex flex-col items-center justify-center flex-1 p-4">
	<section
		id="introPage"
		class="h-screen w-full flex flex-col items-center justify-center text-center sm:pt-28 sm:py-14"
	>
		<div class="flex flex-col items-center justify-center gap-6 md:gap-4 lg:gap-4 -mt-10">
			<h2 class="font-semibold text-4xl sm:text-5xl md:text-6xl">
				Welcome to <span class="poppins text-violet-400">writeme</span>
			</h2>
			<p class="text-base sm:text-lg md:text-xl">
				Use <span class="text-violet-400">AI agents</span> to read your codebase and produce a readme.md
				file.
			</p>
		</div>

<form
    on:submit|preventDefault={handleSubmit}
    class="flex flex-col items-center justify-center gap-4 pt-10"
>
    <input
        type="email"
        bind:value={email}
        placeholder="Enter your email"
        class="input bg-gray-200 px-4 py-2 rounded-md lg:w-96 sm:w-48 md:w-64 focus:outline-none focus:ring-2 focus:ring-violet-400 text-black"
        required
    />
    <input
        type="text"
        bind:value={repositoryName}
        placeholder="exampleOrg/exampleRepo"
        class="input bg-gray-200 px-4 py-2 rounded-md lg:w-96 sm:w-48 md:w-64 focus:outline-none focus:ring-2 focus:ring-violet-400 text-black"
        required
    />
    <input
        type="text"
        bind:value={openaiApiKey}
        placeholder="Enter your OpenAI API key"
        class="input bg-gray-200 px-4 py-2 rounded-md lg:w-96 sm:w-48 md:w-64 focus:outline-none focus:ring-2 focus:ring-violet-400 text-black"
        required
    />
    <select
        bind:value={openaiModel}
        class="input bg-gray-200 px-4 py-2 rounded-md lg:w-96 sm:w-48 md:w-64 focus:outline-none focus:ring-2 focus:ring-violet-400 text-black"
        required
    >
        <option value="" disabled selected>Select OpenAI model</option>
        <option value="gpt-4o-mini">GPT-4o Mini</option>
        <option value="gpt-4o">GPT-4o</option>
        <option value="gpt-4">GPT-4</option>
        <option value="gpt-3.5">GPT-3.5</option>
    </select>
    <button
        type="submit"
        class="bg-violet-400 hover:bg-violet-500 text-white font-bold py-2 px-4 mt-5 rounded-md"
        disabled={isLoading}
    >
        {#if isLoading}
            Processing...
        {:else}
            Submit
        {/if}
    </button>
    {#if message}
        <p class="text-md mt-4 {response.ok ? 'text-green-500' : 'text-red-500'}">{message}</p>
    {/if}
</form>
	</section>

	<section
		id="about"
		class="h-screen lg:pt-16 lg:py-32 flex flex-col gap-16 sm:gap-20 md:gap-24 relative"
	>
		<div class="flex flex-col gap-2 text-center">
			<h3 class="font-semibold text-3xl sm:text-4xl md:text-5xl">What is writeme?</h3>
		</div>

		<div
			class="-mt-10 flex flex-col gap-2 text-center relative before:absolute before:top-0 before:left-0 before:w-2/3 before:h-1.5 before:bg-violet-700 after:absolute after:bottom-0 after:right-0 after:w-2/3 after:h-1.5 after:bg-violet-700 py-4"
		>
			<div class="flex flex-col gap-20 w-full mx-auto max-w-[800px]">
				{#each benefits as benefit, index}
					<div class="flex flex-col gap-2 mx-auto">
						<div class="flex items-end gap-4">
							<p class="poppins text-2xl sm:text-5xl md:text-6xl text-slate-500 font-medium">
								{index + 1}. {benefit.metric}
							</p>
							<p class="flex text-xl sm:text-2xl md:text-3xl capitalize pb-1">
								{benefit.name}
							</p>
						</div>
						<p class="text-center italic">- {benefit.description}</p>
					</div>
				{/each}
			</div>
		</div>
	</section>

	<section id="frameworks" class="justify-top flex flex-col gap-24 pb-96 mb-24">
		<div class="flex flex-col gap-2 text-center">
			<h6 class="text-large sm:text-xl md:text-2xl">How does it work?</h6>
			<h3 class="font-semibold text-3xl sm:text-4xl md:text-5xl">Key Frameworks</h3>
		</div>

		<div class="grid grid-cols-1 lg:grid-cols-3 gap-12 lg:gap-10">
			<Step step={steps[0]}>
				<p>
					AI Agents framework provided by <strong class="text-violet-400">Autogen</strong> for reading
					the repository and writing the readme.md file.
				</p>
			</Step>
			<Step step={steps[1]}>
				<p>
					Utilising <strong class="text-violet-400">Microservice Architecture</strong> through the
					use of <strong class="text-violet-400">Docker and Kubernetes</strong> for containerisation
					and orchestration.
				</p>
			</Step>
			<Step step={steps[2]}>
				<p>
					Hosted on AWS with infrastructure built using <strong class="text-violet-400"
						>Terraform and Terragrunt</strong
					> to provide a reliable method of deployment.
				</p>
			</Step>
		</div>
	</section>
</main>
