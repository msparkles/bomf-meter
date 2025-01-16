export const images = (() => {
	const list: string[][] = [];

	for (let x = 1; x <= 6; x++) {
		list.push([]);
		for (let y = 1; y <= 6; y++) {
			list.at(-1)!.push(`images/pfps/${x}-${y}.png`);
		}
	}

	return list;
})();
