<script>
	import CollapsibleList from '$lib/components/CollapsibleList.svelte';

	export let data;

	$: facets = data.facets;
</script>

<div class="flex">
	<div class="fixed top-24 h-full z-40 flex w-96 flex-col">
		<div class="flex grow flex-col gap-y-5 overflow-y-scroll bg-secondary px-6 py-4">
			<form class="min-w-full" action="?/inscriptions">
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
									class="input input-bordered input-primary bg-white w-full max-w-xs rounded-none"
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
									class="input input-bordered input-primary bg-white w-full max-w-xs rounded-none"
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
									class="input input-bordered input-primary bg-white w-full max-w-xs rounded-none"
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
										class="input input-bordered input-primary bg-white w-24 rounded-none"
										placeholder="323"
									/>
									<div class="form-control">
										<label class="label" for="not_before_era_0"
											><input
												type="radio"
												class="radio h-4 w-4 mr-1"
												name="not_before_era"
												value="bce"
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
												class="radio h-4 w-4 mr-1"
												name="not_before_era"
												value="ce"
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
										class="input input-bordered input-primary bg-white w-24 rounded-none"
										placeholder="330"
									/>
									<div class="form-control">
										<label class="label" for="not_after_era_0"
											><input
												type="radio"
												class="radio h-4 w-4 mr-1"
												name="not_after_era"
												value="bce"
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
												class="radio h-4 w-4 mr-1"
												name="not_after_era"
												value="ce"
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
								<div class="border border-stone-300 p-4 rounded mb-2">
									<h2 class="mb-2 font-semibold">City</h2>
									<CollapsibleList items={facets.cities} let:item={city}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`city-${city.id}`}
													type="checkbox"
													name="cities"
													value={city.id}
												/>
												<span class="label-text ml-4">{city.placename}</span>
												<a
													class="cursor-pointer ml-4 text-stone-400 text-sm hover:underline"
													target="_blank"
													href={city.pleiades_ref}>More info</a
												>
											</label>
										</div>
									</CollapsibleList>
								</div>

								<div class="border border-stone-300 p-4 rounded mb-2">
									<h2 class="mb-2 font-semibold">Provenance</h2>
									<CollapsibleList items={facets.provenances} let:item={provenance}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`provenance-${provenance.id}`}
													type="checkbox"
													name="provenances"
													value={provenance.id}
												/>
												<span class="label-text ml-4">{provenance.placename}</span>
											</label>
										</div>
									</CollapsibleList>
								</div>

								{#if facets.regions && facets.regions.length > 0}
									<div class="border border-stone-300 p-4 rounded">
										<h2 class="mb-2 font-semibold">Region</h2>
										<CollapsibleList items={facets.regions} let:item={region}>
											<div class="form-control">
												<label class="label justify-start">
													<input
														class="checkbox rounded-none h-4 w-4"
														id={`region-${region.id}`}
														type="checkbox"
														name="regions"
														value={region.id}
													/>
													<span class="label-text ml-4">{region.placename}</span>
												</label>
											</div>
										</CollapsibleList>
									</div>
								{/if}
							</div>
						</div>
						<div class="divider" />
						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Type of Inscription</div>
							<div class="collapse-content">
								<div class="border border-stone-300 p-4 rounded">
									<CollapsibleList items={facets.genres} let:item={genre}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`genre-${genre.id}`}
													type="checkbox"
													name="genres"
													value={genre.id}
												/>
												<span class="label-text ml-4">{genre.description || genre.xml_id}</span>
											</label>
										</div>
									</CollapsibleList>
								</div>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Physical Type</div>
							<div class="collapse-content">
								<div class="border border-stone-300 p-4 rounded">
									<CollapsibleList items={facets.physical_types} let:item={physical_type}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`physical_type-${physical_type.id}`}
													type="checkbox"
													name="physical_types"
													value={physical_type.id}
												/>
												<span class="label-text ml-4"
													>{physical_type.description || physical_type.xml_id}</span
												>
											</label>
										</div>
									</CollapsibleList>
								</div>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Language</div>
							<div class="collapse-content">
								<div class="border border-stone-300 p-4 rounded">
									<CollapsibleList items={facets.languages} let:item={language}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`language-${language.id}`}
													type="checkbox"
													name="languages"
													value={language.id}
												/>
												<span class="label-text ml-4">{language.label || language.short_form}</span>
											</label>
										</div>
									</CollapsibleList>
								</div>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Religion</div>
							<div class="collapse-content">
								<div class="border border-stone-300 p-4 rounded">
									<CollapsibleList items={facets.religions} let:item={religion}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`religion-${religion.id}`}
													type="checkbox"
													name="religions"
													value={religion.id}
												/>
												<span class="label-text ml-4"
													>{religion.description || religion.xml_id}</span
												>
											</label>
										</div>
									</CollapsibleList>
								</div>
							</div>
						</div>
						<div class="divider" />

						<div class="font-small collapse collapse-arrow">
							<input type="checkbox" />
							<div class="collapse-title font-medium">Material</div>
							<div class="collapse-content">
								<div class="border border-stone-300 p-4 rounded">
									<CollapsibleList items={facets.materials} let:item={material}>
										<div class="form-control">
											<label class="label justify-start">
												<input
													class="checkbox rounded-none h-4 w-4"
													id={`material-${material.id}`}
													type="checkbox"
													name="materials"
													value={material.id}
												/>
												<span class="label-text ml-4"
													>{material.description || material.xml_id}</span
												>
											</label>
										</div>
									</CollapsibleList>
								</div>
							</div>
						</div>
						<div class="pb-24">
							<button class="btn btn-primary mt-8 rounded-none w-full">Search</button>
						</div>
					</div>
				</div>
			</form>
		</div>
	</div>

    <slot />
</div>
