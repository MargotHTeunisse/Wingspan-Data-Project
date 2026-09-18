nest_capacities = document.getElementsByClassName('nest_capacity')
for (let i = 0; i < nest_capacities.length; i++) {
    let eggs = parseInt(nest_capacities[i].textContent)
    nest_capacities[i].textContent = "🥚".repeat(eggs)
}