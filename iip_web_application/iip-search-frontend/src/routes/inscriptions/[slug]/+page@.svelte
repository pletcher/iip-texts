<script>
	import '../../../app.css';
	export let data;

	$: inscription = data.inscription;
</script>

<div id="single_inscription" class="my-32">
	<div class="w-full px-16 max-w-7xl mx-auto">
		<div class="w-full flex flex-nowrap">
			<div class="flex flex-col w-2/3 px-16">
				<h1 class="font-sans text-2xl mb-4">
					{inscription.filename}
					{inscription.short_description || ''}
				</h1>

				{#each inscription.editions as edition}
					<div class="pb-8">
						<h2 class="font-sans_bold uppercase prose prose-sm prose-stone-500">
							{edition.edition_type.replace('_', ' ')} <a
								href="#bibliography"
								class="underline hover:no-underline prose prose-sm capitalize prose-stone-400 ml-1 font-sans"
								>Source</a
							>
						</h2>
						<p class="font-serif prose-3xl">
							{#if edition.text}
								{edition.text}
							{:else}
								<span class="font-sans text-lg text-gray-500">No {edition.edition_type.replace('_', ' ')}</span>
							{/if}
						</p>
					</div>
				{/each}
			</div>
			<!-- IMAGES -->
			<!-- <div class="w-1/3">
          {% for filename, caption in image_dict.items %}
          <a href="{{image_url_base}}{{filename}}" class="block w-full cursor-zoom-in opacity-100 hover:opacity-80 transition-opacity" onclick="return hs.expand(this)" title="{{caption}}">
            <img width="w-full object-contain " style="max-height:66vh" src="{{image_url_base}}{{filename}}" alt="Highslide JS" title="Click to enlarge">
            <br />
            {{caption}}
          </a>
          {% empty %}
          <img src='{% static "/resources/img/noimg.png" %}' style="width: 150px;">
          {% endfor %}

          {% if image_caption %}
          <div class="">{{ image_caption }}</div>
          {% endif %}

          {% if i.image %}
          <p class="">
            {% for thumb in i.image %}
            <a href="/django_z_media/iip_z_media/inscription_images/display_size/{{thumb}}.jpg"><img onerror="ImgError(this)" src="/django_z_media/iip_z_media/inscription_images/thumbnails/{{thumb}}_t.jpg" /></a><br />
            {% endfor %}
          </p>
          {% endif %}
        </div> -->
		</div>

		<div class="w-full mt-4 px-16">
			<p class="prose prose-stone max-w-prose">
				{inscription.description}
			</p>
		</div>

		<div class="w-full">
			<div
				class="max-w-7 py-10 px-16 my-8 mx-auto flex flex-nowrap justify-around items-center"
				style="background:#e0e0e0;"
			>
				<div class="flex flex-col w-1/4">
					<h2 class="font-sans_bold uppercase text-xs text-gray-500">Languages</h2>

					{#if inscription.languages.length > 0}
						<!-- {% if i.language_display|length > 0 and i.language|length > 0 %}s{% endif %}: -->
						{#each inscription.languages as language}
							<p class="prose prose-sm prose-stone">{language.label}</p>
						{/each}
					{:else}
						<p class="prose prose-sm prose-stone">Language information not available</p>
					{/if}
				</div>

				<div class="flex flex-col w-1/4">
					<h2 class="font-sans_bold uppercase text-xs text-gray-500">Dimensions</h2>

					<p>
						<!-- {% if i.dimensions %}
              {{i.dimensions}}
              {% else %}
              Not Available
              {% endif %} -->
					</p>
				</div>

				<div class="flex flex-col w-1/4">
					<h2 class="font-sans_bold uppercase text-xs text-gray-500">Date</h2>

					<p>
						<!-- {% if i.notBefore %}
              {{i.notBefore|cleanDates}} to {{i.notAfter|cleanDates}}
              {% else %}
              Not Available
              {% endif %} -->
					</p>
				</div>

				<!-- MINI MAP -->

				<!-- <script type="text/javascript">
            var inscription_list = ["{{i.inscription_id}}"];
          </script>

          <div class="flex flex-col w-1/4">
            <script src='https://api.mapbox.com/mapbox-gl-js/v0.38.0/mapbox-gl.js'></script>
            <script src="https://unpkg.com/leaflet@1.0.3/dist/leaflet.js" integrity="sha512-A7vV8IFfih/D732iSSKi20u/ooOfj/AGehOKq0f4vLT1Zr2Y+RX7C+w8A1gaSasGtRUZpF/NZgzSAu4/Gc41Lg==" crossorigin=""></script>
            <script src="https://code.jquery.com/jquery-1.12.1.min.js"></script>

            <script type="text/javascript">
              var API_URL = "{% url 'api_wrapper' %}";
            </script> 

            <script type="text/javascript" src='{% static "iip_search_app/js/maplet.js" %}'></script>
            <div id="maplet{{i.inscription_id}}" class="" style="    width: 100%;
                height: 120px;
                display: block;
                border: 1px solid #aaa;
                margin-bottom: 10px;"></div>


            <h2 class="font-sans_bold uppercase text-xs text-gray-500">Place Found</h2>
            <p>
              {% if i.place_found %}
              {{i.place_found|placeClean}}
              {% else %}
              Not Available
              {% endif %}
            </p>
          </div>

        </div> -->
				<div class="max-w-7xl px-16 my-4 mx-auto">
					<div class="flex flex-col mb-4">
						<h2 class="font-sans_bold uppercase text-xs text-gray-500">Current Location</h2>
						<p>
							<!-- {% if i.provenance %}
              {{ i.provenance.0 }}
              {% else %}
              Not Available
              {% endif %} -->
						</p>
					</div>

					<div class="flex flex-col mb-4">
						<h2 class="font-sans_bold uppercase text-xs text-gray-500">Figures</h2>
						<p>
							<!-- {% if i.figure %}{% for f in i.figure %}{{f}}<br />{% endfor %}{% else %}Not Available{% endif %}</p> -->
						</p>
					</div>

					<div id="bibliography">
						<div class="flex flex-col mb-4">
							<h2 class="font-sans_bold uppercase text-xs text-gray-500">
								Source of Diplomatic <a
									href="#bibliography"
									class="underline hover:no-underline text-xs capitalize text-gray-400 ml-1 font-sans"
									>Zotero</a
								>
							</h2>
							<p>
								<!-- {% if biblDiplomatic %}
                <span id="diplomatic" class="" bibl='{{biblDiplomatic.0}}' ntype='{{biblDiplomatic.1}}' n='{{biblDiplomatic.2}}'>{{biblDiplomatic}}</span>

                {% else %}
                Not available
                {% endif %} -->
							</p>
						</div>
						<!-- REPEAT ABOVE FOR ALL EDITIONS -->

						<!-- HIDE IF NO FULL BIBLIOGRAPHY-->
						<div class="flex flex-col mb-4">
							<h2 class="font-sans_bold uppercase text-xs text-gray-500">
								Bibliography <a
									href="#bibliography"
									class="underline hover:no-underline text-xs capitalize text-gray-400 ml-1 font-sans"
									>Zotero</a
								>
							</h2>
							<p>
								<!-- <ol id="" class='' style="{% if not biblioFull %}display: none;{% endif %}"> -->

								<!-- 
                  {% for bib_id, reference in z_ids.items %}

                  <div class="" style="">
                    <div>

                      <span style="" class='z_id' bibl='{{bib_id}}'>{{bib_id}}</span>
                      <span class='ref' style="display:inline; white-space:nowrap; position:relative;">
                        {% for ntype, n in reference %}

                        {% if ntype == 'insc' %}
                        insc.
                        {% elif ntype == 'page' %}
                        p.
                        {% else %}
                        {{ntype}}
                        {% endif %}
                        {% if n == reference|last|last %}
                        {{n}}
                        {% else %}
                        {{n}};
                        {% endif %}
                        {% endfor %}
                        )
                      </span>

                    </div>

                  </div>
                  {% endfor %}



                </ol> -->
							</p>
							<!--           {% if biblioFull %}
          <p><span class="short_header"><span style="font-weight: bold;">Bibliography: </span></span>Not Available</p>
        {% endif %} -->
						</div>

						<div style="clear:both" />

						<!-- {% if not biblioFull %}<div id="permalink"><a href="../viewinscr/{{i.inscription_id}}/">Link to this inscription</a></div>{% endif %} -->

						<div
							class="font-sans uppercase underline hover:no-underline text-sm my-4 text-theme-700"
						>
							<a href="#XML">View XML</a>
						</div>
					</div>

					<!-- TODO: FIX ZOTERO CITATIONS -->

					<h2>Cite This Inscription</h2>

					<p class="pb-2">
						IIP is committed to the idea that the public good is best served by keeping our data
						free for use and reuse. You can cite and use this inscription under the terms of the
						Creative Commons Attribution-NonCommercial 4.0 International License. Note also that all
						images are either in the public domain or used with permission, and unless noted we do
						not hold copyright to them. For permission to reuse the images, please contact the
						copyright holder, noted in the illustration credit.
					</p>

					<p class="pb-2">
						The project can be cited as: Satlow, Michael L., ed. 2002 - . “Inscriptions of
						Israel/Palestine.” Brown University. <a href="https://doi.org/10.26300/PZ1D-ST89"
							>https://doi.org/10.26300/PZ1D-ST89</a
						>
					</p>

					<p class="pb-2">
						This inscription can be cited as: "Inscriptions of Israel/Palestine," [inscription
						id],[today's date]. https:doi.org/10.26300/pz1d-st89
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
