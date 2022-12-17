<script>
  import LeaderboardItem from '$lib/components/LeaderboardItem.svelte';

  export let emojis;
  export let leaderboard;
  export let limit = 10;
  export let offset = 0;
</script>

<table class="flex flex-col space-y-3 w-full sm:w-4/5 md:w-3/5 lg:w-2/5">
  {#each [...Object.entries(leaderboard).entries()].slice(offset, limit) as [idx, [emoji, uses]] (emoji)}
    <LeaderboardItem
      names={[emoji, ...emojis[emoji].aliases]}
      iconUrl={emojis[emoji].url}
      position={idx}
      {uses}
    />
  {/each}
</table>
