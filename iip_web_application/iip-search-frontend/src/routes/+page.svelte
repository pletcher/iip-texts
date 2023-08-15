<script>
	import SearchMap from './SearchMap.svelte';

	export let data;
</script>

<div>
	<div class="fixed inset-y-0 z-50 flex w-96 flex-col">
		<div class="flex grow flex-col gap-y-5 overflow-y-auto bg-secondary px-6 pb-4">
			<div class="flex h-24 shrink-0 items-center">
				<img
					class="h-16 pt-1 w-auto"
					src="img/iip_logo.jpg"
					alt="Inscriptions from Israel and Palestine"
				/>
			</div>
			<form class="min-w-full">
				<div>
					<div class="border-b border-gray-900/10 pb-12">
						<h2 class="font-semibold underline leading-7 hover:text-neutral-500">
							<a href="//www.inscriptionsisraelpalestine.org/guide-to-searching/"
								>Guide to Searching</a
							>
						</h2>

						<div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
							<div class="col-span-full">
								<label for="text_search" class="label">
									<span class="label-text">Text or translation</span>
								</label>
								<input
									type="text"
									name="text_search"
									id="text_search"
									class="input input-bordered input-primary bg-white w-full max-w-xs"
									placeholder="λόγος καὶ ἔργα"
								/>
							</div>

							<div class="col-span-full">
								<label for="description_place_id" class="label">
									<span class="label-text">Description/Place/ID</span>
								</label>
								<input
									type="text"
									name="description_place_id"
									id="description_place_id"
									class="input input-bordered input-primary bg-white w-full max-w-xs"
									placeholder="Egypt"
								/>
							</div>

							<div class="col-span-full">
								<label for="figures" class="label">
									<span class="label-text">Figures</span>
								</label>

								<input
									type="text"
									name="figures"
									id="figures"
									class="input input-bordered input-primary bg-white w-full max-w-xs"
									placeholder="grapevine"
								/>
							</div>

							<div class="col-span-full grid-cols-3">
								<label for="not_before" class="label"><span class="label-text">From</span></label>
								<div class="flex">
									<input
										type="number"
										name="not_before"
										min="-2000"
										max="2000"
										step="1"
										id="not_before"
										class="input input-bordered input-primary bg-white"
										placeholder="-323"
									/>
									<div class="form-control">
										<label class="label" for="not_before_era_0"
											><input
												type="radio"
												class="radio"
												name="not_before_era"
												id="not_before_era_0"
												checked
											/>
											<span class="label-text cursor-pointer">BCE</span></label
										>
									</div>
									<div>
										<label class="label" for="not_before_era_1"
											><input
												type="radio"
												class="radio"
												name="not_before_era"
												id="not_before_era_1"
											/>
											<span class="label-text cursor-pointer">CE</span></label
										>
									</div>
								</div>
							</div>

							<div class="col-span-full grid-cols-3">
								<label for="not_after" class="label"><span class="label-text">To</span></label>
								<div class="flex">
									<input
										type="number"
										name="not_after"
										min="-2000"
										max="2000"
										step="1"
										id="not_after"
										class="input input-bordered input-primary bg-white"
										placeholder="330"
									/>
									<div class="form-control">
										<label class="label" for="not_after_era_0"
											><input
												type="radio"
												class="radio"
												name="not_after_era"
												id="not_after_era_0"
												checked
											/>
											<span class="label-text cursor-pointer">BCE</span></label
										>
									</div>
									<div>
										<label class="label" for="not_after_era_1"
											><input
												type="radio"
												class="radio"
												name="not_after_era"
												id="not_after_era_1"
											/>
											<span class="label-text cursor-pointer">CE</span></label
										>
									</div>
								</div>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Location</div>
							<div class="collapse-content">
								<div>
									<h2>City</h2>
									<ul>
										{#each data.cities as { id, placename, pleiades_ref }}
											<li>
												<div class="form-control">
													<label class="label justify-start">
														<input
															class="checkbox"
															id={`city-${id}`}
															type="checkbox"
															value={`city-${id}`}
														/>
														<span class="label-text ml-4">{placename}</span>
														<a
															class="cursor-pointer ml-4 text-stone-400 text-sm hover:underline"
															target="_blank"
															href={pleiades_ref}>More info</a
														>
													</label>
												</div>
											</li>
										{/each}
									</ul>
								</div>
							</div>
						</div>
						<div class="divider" />
						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Type of Inscription</div>
							<div class="collapse-content">
								<p>hello</p>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Physical Type</div>
							<div class="collapse-content">
								<p>hello</p>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Language</div>
							<div class="collapse-content">
								<p>hello</p>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Religion</div>
							<div class="collapse-content">
								<p>hello</p>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Material</div>
							<div class="collapse-content">
								<p>hello</p>
							</div>
						</div>
					</div>
				</div>
			</form>
		</div>
	</div>

	<div class="lg:pl-72">
		<div class="sticky top-0 z-40 flex h-16 shrink-0 items-center bg-primary">
			<button type="button" class="-m-2.5 p-2.5 text-gray-700 lg:hidden">
				<span class="sr-only">Open sidebar</span>
				<svg
					class="h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
					stroke-width="1.5"
					stroke="currentColor"
					aria-hidden="true"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
					/>
				</svg>
			</button>

			<!-- Separator -->
			<div class="h-6 w-px bg-gray-900/10 lg:hidden" aria-hidden="true" />

			<div class="absolute right-0 flex space-x-10 pr-4 text-white">
				<a
					class="cursor-pointer hover:text-base-300 hover:underline"
					href="//inscriptionsisraelpalestine.com/about">About</a
				>
				<a
					class="cursor-pointer hover:text-base-300 hover:underline"
					href="//inscriptionsisraelpalestine.com/about">Stories</a
				>
				<a
					class="cursor-pointer hover:text-base-300 hover:underline"
					href="//inscriptionsisraelpalestine.com/about">Resources</a
				>
				<a
					class="cursor-pointer hover:text-base-300 hover:underline"
					href="//inscriptionsisraelpalestine.com/about">Contact</a
				>
			</div>
		</div>

		<main class="py-10">
			<div class="px-4 sm:px-6 lg:px-8">
				<slot />
				<SearchMap />
			</div>
		</main>
	</div>
</div>
