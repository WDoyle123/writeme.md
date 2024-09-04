<script>
    export let currentYear = new Date().getFullYear();
</script>

<div class="py-5 border-t border-solid border-violet-950 flex flex-col gap-4 sm:gap-8 justify-center items-center">
    <div class="flex flex-col gap-4 items-center justify-center">
        <div class="flex items-center gap-4 sm:gap-6 text-2xl sm:text-3xl md:text-4xl mx-auto">
            <a href="https://www.linkedin.com/in/william-doyle-489750239/" class="hover:text-blue-700" aria-label="LinkedIn">
                <i class="fa-brands fa-linkedin-in"></i>
            </a>
            <a href="https://github.com/WDoyle123" class="hover:text-gray-700" aria-label="GitHub">
                <i class="fa-brands fa-github"></i>
            </a>
        </div>
        <p>© <span>{currentYear}</span> writeme.md. All rights reserved.</p>
    </div>
</div>

