# Slop-to-simple substitutions

This table maps words that AI-generated text overuses to plain replacements. If the word carries no fact, delete it instead of replacing it.

| Slop | Write instead |
|---|---|
| leverage, utilize | use |
| in order to | to |
| prior to | before |
| ensure | make sure that |
| it is worth noting that | (delete) |
| it's important to | (delete — state the fact) |
| simply, just, easily, seamless, seamlessly, effortlessly | (delete) |
| robust, powerful, comprehensive, performant | (delete, or give the measurable property) |
| functionality | function, feature |
| enables you to, allows you to | you can |
| is designed to, aims to | (delete — say what it does) |
| facilitate | help, make possible |
| dive into, delve into | read, examine |
| when it comes to | for |
| in the event that | if |
| due to the fact that | because |
| as needed, as necessary | (state the condition) |
| and/or | Pick one, or write "X, or Y, or both" |
| e.g. / i.e. / etc. | for example / that is / (name the items) |
| gracefully handles | (say what it does: "retries three times, then stops") |
| out of the box | by default |
| under the hood | internally |
| blazingly fast | fast (give the number) / (delete) |
| streamline | make simpler, make faster |
| plethora, myriad | many |
| addresses the issue, tackles | corrects the fault, removes the error |
| pivotal, crucial, crucially, paramount | important |
| tapestry, testament, synergy | (delete) |
| interplay | interaction (or delete) |
| intricate | complex |
| vibrant, nuanced, multifaceted | (delete, or name the parts) |
| realm, landscape (metaphorical) | area |
| groundbreaking, cutting-edge, state-of-the-art, innovative, unprecedented | new (or delete) |
| transformative, game-changer | (delete — say what changes) |
| revolutionize | change |
| showcase, underscore, emphasize | show |
| foster, empower, bolster | help, support, let |
| harness | use |
| enhance | improve |
| elevate | increase |
| furthermore, moreover | also |
| in conclusion, in summary, at the end of the day | (delete) |
| embark, endeavor | start, try |
| meticulous, meticulously | careful, carefully |
| holistic | full |
| paradigm | model |
| navigate (metaphorical) | go to |
| boasts | has |
| nestled, in the heart of | (delete — give the location or the fact) |
| bustling | busy |
| that being said, notwithstanding | but |
| I hope this helps, let's dive in | (delete) |
| substrate | base |
| wedge, wedge in | add, insert |
| vector (metaphorical) | way, method |
| locus, nexus | center, connection |
| primitive (as a noun) | basic type, building block |
| bedrock, scaffolding (metaphorical) | foundation, structure |
| modality | mode, form |
| gold-plating | over-engineering, unnecessary extras |
| evacuate (for code) | move out, migrate |
| endgame | final phase, goal |
| north star, flywheel | goal, momentum (or delete) |
| stands as, serves as | is |
| not just X, but Y | (state the point directly) |

---

## Syntactic & Stylistic AI Tells (De-slopping Rules)

1. **Em Dash Elimination (`—`)**:
   - Avoid em dashes entirely. Em dashes are the most recognizable syntactic marker of AI text.
   - If a thought needs separation, end the sentence with a period and start a fresh sentence.
   - If joining dependent clauses, use a comma with a concrete conjunction (*"because"*, *"but"*, *"so"*).
2. **Colon-as-Connector Ban**:
   - Colons belong before a vertical list or explicit code example.
   - Do NOT use colons as mid-sentence connectors between clauses (e.g. *"If tests pass: the deployment begins"* $\rightarrow$ *"When tests pass, deployment begins"*).
3. **Superficial -ing Participles**:
   - Eliminate dangling trailing participial phrases (*"...highlighting key components"*, *"...ensuring high performance"*, *"...reflecting best practices"*).
   - State the actor and direct action as a complete sentence or clause.
4. **Vague Attributions**:
   - Eliminate *"industry reports suggest"*, *"experts believe"*, *"some critics argue"*.
   - Name the concrete source, or delete the claim.
5. **False Ranges**:
   - Avoid *"ranging from X to Y"* unless X and Y exist on a meaningful quantitative or scalar continuum. List topics directly.
6. **Chatbot Pleasantries & Sycophancy**:
   - Delete *"Of course!"*, *"Certainly!"*, *"Great question!"*, *"You're absolutely right!"*, *"Found the smoking gun!"*.
   - Respond directly with technical substance without conversational buffering.
7. **Say What It Does, Not How It Feels**:
   - Replace emotive feeling words (*"the database stays close at hand"*, *"SQL you can love"*) with concrete mechanisms and numbers (*"`.toSQL()` returns the exact string sent to PostgreSQL"*, *"column renames fail compilation"*).
   - If a sentence could appear unchanged in another completely unrelated repository's documentation, it says nothing about this one—delete it.
