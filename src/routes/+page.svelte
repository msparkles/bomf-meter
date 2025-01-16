<script lang="ts">
	import { images } from '$lib';
	import Bomf from './bomf.svelte';

	let blendModes = [
		'normal',
		'multiply',
		'screen',
		'overlay',
		'darken',
		'lighten',
		'color-dodge',
		'color-burn',
		'hard-light',
		'soft-light',
		'difference',
		'exclusion',
		'hue',
		'saturation',
		'color',
		'luminosity',
		'plus-darker',
		'plus-lighter'
	];

	let blendMode = $state('normal');

	let MAX_X = 500.0;
	let MAX_Y = 500.0;

	let interpolaterSelecting = $state(false);

	let interpolatorXRaw = $state(MAX_X / 2);
	let interpolatorXTotal = $derived(interpolatorXRaw / MAX_X);
	let interpolatorXPos = $derived(interpolatorXRaw / 100.0);
	let interpolatorXLocal = $derived(interpolatorXPos - Math.floor(interpolatorXPos));

	let interpolatorYRaw = $state(MAX_Y / 2);
	let interpolatorYTotal = $derived(interpolatorYRaw / MAX_Y);
	let interpolatorYPos = $derived(interpolatorYRaw / 100.0);
	let interpolatorYLocal = $derived(interpolatorYPos - Math.floor(interpolatorYPos));

	function normalizePos() {
		interpolatorXRaw = Math.max(0, Math.min(interpolatorXRaw, MAX_X));
		interpolatorYRaw = Math.max(0, Math.min(interpolatorYRaw, MAX_Y));
	}

	function handleMove(event: PointerEvent) {
		let rect = document.getElementById('interpolator-selector')!.getBoundingClientRect();

		interpolatorXRaw = ((event.clientX - rect.x) / rect.width) * MAX_X;
		interpolatorYRaw = ((event.clientY - rect.y) / rect.height) * MAX_Y;

		normalizePos();
	}

	let xIdx = () => Math.floor(interpolatorXPos);
	let xNext = () => Math.max(0, Math.min(xIdx() + 1, images.length - 1));

	let yIdx = () => Math.floor(interpolatorYPos);
	let yNext = () => Math.max(0, Math.min(yIdx() + 1, images[xIdx()].length - 1));
</script>

<svelte:head>
	<title>the BOMF meter !! :3</title>
	<meta content="the BOMF meter !! :3" property="og:title" />
	<meta
		content="how bomf is bomf at [0.32, 0.76] on the bomf scale??? ? ?"
		property="og:description"
	/>
</svelte:head>

<svelte:body
	onpointermove={(event) => {
		if (!interpolaterSelecting) return;
		handleMove(event);
	}}
	onpointerup={() => {
		interpolaterSelecting = false;
	}}
/>

<main id="column">
	<p class="break-words pb-10 text-center text-5xl font-bold leading-normal">
		THE <Bomf /> METER
	</p>

	<p class="break-words text-center text-2xl font-bold leading-loose">
		now with the
		<Bomf />
		interpolator!!!!!!!!!!!
	</p>

	<div class="relative m-2 flex h-full w-full justify-center">
		<div class="h-auto w-full flex-none p-12">
			<div class="rounded-2xl border-8 border-solid border-fuchsia-300 bg-fuchsia-300 shadow-2xl">
				<div class="bg-grid-gradient grid grid-flow-col grid-rows-6 rounded-xl p-[2%]">
					{#each images as col, x}
						{#each col as image, y}
							<div class="p-[4%]">
								<div class="pfp-btn relative h-full w-full overflow-hidden">
									<div class="absolute left-0 top-0 z-10 h-full w-full bg-black/35"></div>
									<div
										class="relative z-50 aspect-square h-full w-full bg-contain bg-center bg-no-repeat"
										style:background-image={`url(${image})`}
									></div>
								</div>
							</div>
						{/each}
					{/each}
				</div>
			</div>
		</div>

		<code
			class="absolute left-0 top-0 flex h-full w-8 flex-col items-center justify-center gap-3 py-12 text-center text-xs"
		>
			HIGH ENERGY
			<div class="h-full w-px rounded border-x-2 border-solid border-pink-400"></div>
			LOW ENERGY
		</code>

		<code
			class="absolute bottom-0 left-0 flex h-8 w-full flex-row items-center justify-center gap-3 px-12 text-center text-xs"
		>
			UNPLEASANT
			<div class="h-px w-full rounded border-y-2 border-solid border-pink-400"></div>
			PLEASANT
		</code>
	</div>

	<br />
	<br />
	<br />

	<p class="break-words pb-4 text-center text-4xl font-bold leading-normal">
		and now................................................................................
	</p>

	<p class="break-words pb-10 text-center text-5xl font-bold leading-normal">
		THE
		<Bomf />
		INTERPOLATOR!!111!!!11111!!!!!1
	</p>

	<div class="relative flex h-full w-full select-none justify-center" aria-hidden="true">
		<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
		<div
			id="interpolator-selector"
			class="bg-grid-gradient relative mx-20 mt-12 aspect-square h-auto w-full max-w-[512px] cursor-crosshair touch-none"
			oncontextmenu={(event) => event.preventDefault()}
			onpointerdown={(event) => {
				interpolaterSelecting = true;
				handleMove(event);
			}}
			onkeydown={(event) => {
				switch (event.key) {
					case 'ArrowDown':
						interpolatorXRaw += 5;
						break;
					case 'ArrowUp':
						interpolatorXRaw -= 5;
						break;
					case 'ArrowRight':
						interpolatorYRaw += 5;
						break;
					case 'ArrowLeft':
						interpolatorYRaw -= 5;
						break;
					default:
						return;
				}

				event.preventDefault();

				normalizePos();
			}}
			tabindex={0}
			aria-hidden="true"
		>
			<div
				style:left={`${interpolatorXTotal * 100.0}%`}
				style:top={`${interpolatorYTotal * 100.0}%`}
				class="pointer-events-none absolute h-[2.5%] w-[2.5%] -translate-x-1/2 -translate-y-1/2 select-none rounded-full bg-gray-600"
			></div>

			<code class="absolute -top-8 left-0 h-min whitespace-pre">
				{Math.round((1.0 - interpolatorYTotal) * 100)
					.toString()
					.padStart(3, ' ')}% E
			</code>

			<code class="absolute -left-12 top-2 -translate-x-1/2 whitespace-pre">
				{Math.round(interpolatorXTotal * 100)
					.toString()
					.padStart(3, ' ')}% P
			</code>
		</div>
	</div>

	<div class="mx-auto my-6" aria-hidden="true">
		<label class="block break-words text-center text-xl leading-[3]" for="blend-mode">
			how would you like to <i><em>blend</em></i> your <Bomf />
		</label>

		<select
			class="mx-auto my-4 block rounded border-2 border-solid border-purple-300 bg-slate-800 p-2"
			name="blend-mode"
			id="blend-mode"
			onchange={(event) => (blendMode = (event.target as HTMLSelectElement).value)}
		>
			{#each blendModes as option}
				<option value={option}>{option}</option>
			{/each}
		</select>
	</div>

	<div
		class="relative mx-auto aspect-square h-auto w-full max-w-[512px] flex-none bg-white"
		style:mix-blend-mode={blendMode}
		aria-hidden="true"
	>
		<img
			id="interpolator-x0-y0"
			class="absolute left-0 top-0 h-full w-full"
			style:opacity={(1.0 - interpolatorXLocal) * (1.0 - interpolatorYLocal)}
			src={images[xIdx()][yIdx()]}
			alt=""
		/>

		<img
			id="interpolator-x1-y0"
			class="absolute left-0 top-0 h-full w-full"
			style:opacity={interpolatorXLocal * (1.0 - interpolatorYLocal)}
			src={images[xNext()][yIdx()]}
			alt=""
		/>

		<img
			id="interpolator-x0-y1"
			class="absolute left-0 top-0 h-full w-full"
			style:opacity={(1.0 - interpolatorXLocal) * interpolatorYLocal}
			src={images[xIdx()][yNext()]}
			alt=""
		/>

		<img
			id="interpolator-x1-y1"
			class="absolute left-0 top-0 h-full w-full"
			style:opacity={interpolatorXLocal * interpolatorYLocal}
			src={images[xNext()][yNext()]}
			alt=""
		/>
	</div>
</main>
