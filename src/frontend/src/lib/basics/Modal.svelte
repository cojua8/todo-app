<div
  on:click
  on:keydown
  role="button"
  tabindex="0"
  class="bg-black fixed left-0 top-0 w-screen h-screen z-40 opacity-50 cursor-default"
/>
<div class="relative z-50 bg-white rounded-xl {$$restProps.class}">
  <div class="p-2">
    <slot />
  </div>
</div>
