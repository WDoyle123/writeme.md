<script>
    export let y;

    export let tabs = [
        { name: "GitHub", link: "https://github.com/WDoyle123/writeme" },
    ];
</script>

<header
    class={"sticky z-[10] top-0 duration-200 px-6 flex items-center justify-between border-b border-solid " +
        (y > 0
            ? " py-4 bg-slate-950 border-violet-950"
            : " py-6 bg-transparent border-transparent")}
>
    <h1 class="font-medium">
        <b class="font-bold poppins">writeme</b><span class="">.md</span>
    </h1>

    <div class="flex items-center gap-4">
        {#each tabs as tab, index}
            <a
                href={tab.link}
                class="duration-200 hover:text-violet-400"
                target={index === 2 ? "_blank" : ""}
            >
                <p>{tab.name}</p>
            </a>
	{/each}

        <button
            class="blueShadow relative overflow-hidden px-5 py-2 group rounded-full bg-white text-slate-950">
            <div class="absolute top-0 right-full w-full h-full bg-violet-400 opacity-20 group-hover:translate-x-full z-0 duration-200"/>
		    <h4 class="relative z-9"><a href="mailto:william.e.doyle.contact@gmail.com">Contact</h4>
	</button>

    </div>
</header>
