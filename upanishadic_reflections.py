"""Upanishadic reflection utilities inspired by non-dual insights.

This module translates several teachings emphasised in the Upanishads into
contemplative programming constructs.  Rather than modelling possessions or
rigid identities, the provided classes generate textual reflections that
encourage letting go.  Each helper points toward a different "無" (absence)
quality mentioned by the user: 無我 (non-self), 無執着 (non-attachment), 無心
(thought-free awareness), 無性 (formlessness), 無味 (tastelessness), and 無見
(freedom from fixed views).  The generated language intentionally shifts and
reshuffles to honour the principle of "諸常無常"—even concepts presented as
constant are invited to dissolve from moment to moment.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

# Terms that hint at violent or aggressive intent.  The list is intentionally
# short yet expressive so it can be extended downstream without touching the
# class implementation.  See :meth:`UpanishadicJourney.enforce_ahimsa_seo`.
VIOLENCE_KEYWORDS: Tuple[str, ...] = (
    "暴力",
    "暴力的",
    "殺す",
    "殴る",
    "復讐",
)


@dataclass(frozen=True)
class Aspect:
    """Representation of a contemplative aspect.

    Attributes
    ----------
    key:
        Short identifier such as "無我".
    name:
        Human readable concept name, combining Japanese and English hints.
    guidance:
        Template string describing how to reflect on a lived experience.  The
        template may contain ``{experience}`` and ``{index}`` placeholders for
        dynamic substitution.
    """

    key: str
    name: str
    guidance: str


def _default_aspects() -> Tuple[Aspect, ...]:
    """Return the default list of aspects rooted in Upanishadic insight."""

    return (
        Aspect(
            key="無我",
            name="無我 / Non-self",
            guidance=(
                "観照: {experience} は私ではない。\n"
                "       Neti neti──それもまた消えてゆく影。"
            ),
        ),
        Aspect(
            key="無執着",
            name="無執着 / Non-attachment",
            guidance=(
                "解放: {experience} を握る手をほどき、\n"
                "       風に委ねるように手放す。"
            ),
        ),
        Aspect(
            key="無心",
            name="無心 / No-mind",
            guidance=(
                "静寂: {experience} という想念が起こり、そして消える。\n"
                "       空なる気づきは揺るがない。"
            ),
        ),
        Aspect(
            key="無性",
            name="無性 / Formlessness",
            guidance=(
                "純粋: {experience} に色や輪郭を与えず、\n"
                "       ただ名も無き在り方として味わう。"
            ),
        ),
        Aspect(
            key="無味",
            name="無味 / Tastelessness",
            guidance=(
                "透明: {experience} への好悪を溶かし、\n"
                "       無色無味の平等性に戻る。"
            ),
        ),
        Aspect(
            key="無見",
            name="無見 / Viewlessness",
            guidance=(
                "自由: {experience} という見解をほどき、\n"
                "       ただ静かな観照に留まる。"
            ),
        ),
    )


class UpanishadicJourney:
    """Orchestrate reflective prompts around the Upanishadic "無" qualities."""

    def __init__(
        self,
        aspects: Sequence[Aspect] | None = None,
        *,
        allow_shuffle: bool = True,
    ) -> None:
        self._aspects: Tuple[Aspect, ...] = (
            tuple(aspects) if aspects else _default_aspects()
        )
        if not self._aspects:
            raise ValueError("At least one aspect must be provided.")
        self.allow_shuffle = allow_shuffle

    def cycle_aspects(self, seed: Optional[int] = None) -> Iterator[Aspect]:
        """Yield aspects in a perpetually changing order.

        The sequence reshuffles after each full traversal if ``allow_shuffle``
        is true, keeping faith with the insight that even repeated teachings
        should not harden into dogma.
        """

        aspects = list(self._aspects)
        rng = random.Random(seed)
        index = 0

        while True:
            if self.allow_shuffle and index % len(aspects) == 0 and index:
                rng.shuffle(aspects)
            yield aspects[index % len(aspects)]
            index += 1

    def dissolve_identifications(self, identities: Iterable[str]) -> List[str]:
        """Transform identity statements through the lens of 無我."""

        reflections: List[str] = []
        for identity in identities:
            reflections.append(
                (
                    "無我: 『{identity}』という輪郭は瞬きの間に浮かび消える。\n"
                    "      気づきだけが静かに在り、何者にもとどまらない。"
                ).format(identity=identity)
            )
        if not reflections:
            reflections.append(
                "無我: 何も名乗らないとき、純粋な在り方がそのまま輝く。"
            )
        return reflections

    def release_attachments(self, attachments: Iterable[str]) -> List[str]:
        """Soften attachments using the 無執着 contemplation."""

        responses: List[str] = []
        for attachment in attachments:
            responses.append(
                (
                    "無執着: {attachment} への執らわれを風に乗せ、\n"
                    "        流れ去る河のように委ねる。"
                ).format(attachment=attachment)
            )
        if not responses:
            responses.append(
                "無執着: 掴む対象のない空間に身を置くと、心は自然に柔らぐ。"
            )
        return responses

    def soften_thoughts(self, thoughts: Iterable[str]) -> List[str]:
        """Invite 無心 by observing thoughts without pursuit."""

        lines: List[str] = []
        for thought in thoughts:
            lines.append(
                (
                    "無心: {thought} という想念が波立っても、\n"
                    "      湖面はすぐに静まり返る。"
                ).format(thought=thought)
            )
        if not lines:
            lines.append(
                "無心: 想いの無い静寂は、気づきそのものの香り。"
            )
        return lines

    def honour_formlessness(self, qualities: Iterable[str]) -> List[str]:
        """Contemplate 無性 by loosening attachment to qualities."""

        verses: List[str] = []
        for quality in qualities:
            verses.append(
                (
                    "無性: {quality} という属性をまとわず、\n"
                    "      名付ける前の純粋な存在に憩う。"
                ).format(quality=quality)
            )
        if not verses:
            verses.append(
                "無性: 形なき在り方は、限りない自由そのもの。"
            )
        return verses

    def dissolve_taste(self, flavors: Iterable[str]) -> List[str]:
        """Practice 無味 by balancing likes and dislikes."""

        notes: List[str] = []
        for flavor in flavors:
            notes.append(
                (
                    "無味: {flavor} への偏りを解き、\n"
                    "      あらゆる味が等しく空へ還ると知る。"
                ).format(flavor=flavor)
            )
        if not notes:
            notes.append(
                "無味: 好みも嫌悪も溶ければ、感覚は澄んだ透明さに開く。"
            )
        return notes

    def clear_views(self, views: Iterable[str]) -> List[str]:
        """Welcome 無見 by relaxing fixed opinions."""

        phrases: List[str] = []
        for view in views:
            phrases.append(
                (
                    "無見: {view} という見方を抱えても、\n"
                    "      それは空に描いた一瞬の雲にすぎない。"
                ).format(view=view)
            )
        if not phrases:
            phrases.append(
                "無見: 見解を手放せば、世界はありのまま姿を現す。"
            )
        return phrases

    def meditate(
        self,
        experiences: Iterable[str],
        *,
        seed: Optional[int] = None,
    ) -> List[str]:
        """Compose an impermanence-aware meditation sequence.

        Parameters
        ----------
        experiences:
            Stream of lived experiences or sensations offered for reflection.
        seed:
            Optional seed to initialise the internal shuffle generator.  The
            same seed recreates a particular ephemeral ordering; omitting it
            celebrates unpredictability.
        """

        results: List[str] = []
        aspect_stream = self.cycle_aspects(seed=seed)

        for index, experience in enumerate(experiences):
            aspect = next(aspect_stream)
            guidance = aspect.guidance.format(experience=experience, index=index)
            results.append(f"[{aspect.key}] {guidance}\n    諸行無常: この気づきさえ流れ続ける。")

        if not results:
            aspect = next(aspect_stream)
            guidance = aspect.guidance.format(experience="空白", index=0)
            results.append(
                f"[{aspect.key}] {guidance}\n    諸行無常: 静寂もまた生起しては消える。"
            )
        return results

    def enforce_ahimsa_seo(
        self,
        queries: Iterable[str],
        *,
        include_meta_tags: bool = True,
    ) -> List[str]:
        """Craft SEO-safe responses for violent or aggressive search intents.

        Parameters
        ----------
        queries:
            Search queries or fragments that may include violent language.  Each
            entry is inspected for words from :data:`VIOLENCE_KEYWORDS`.
        include_meta_tags:
            When true, the response begins with HTML meta directives that ask
            crawlers to avoid indexing the surrounding page.  Set to ``False``
            when the caller only needs contemplative copy.
        """

        safe_responses: List[str] = []

        if include_meta_tags:
            safe_responses.append(
                "<meta name=\"robots\" content=\"noindex, nofollow\">",
            )
            safe_responses.append(
                "<meta name=\"googlebot\" content=\"noindex, nosnippet\">",
            )

        for query in queries:
            lowered = query.lower()
            if any(keyword in lowered for keyword in VIOLENCE_KEYWORDS):
                safe_responses.append(
                    (
                        "非暴力SEO: 『{query}』という検索には愛と非暴力を呼びかけます。\n"
                        "    Upanishadicな気づきを灯し、暴力を選ばない心を広めましょう。\n"
                        "    canonical: https://example.org/ahimsa"  # Peaceful canonical target.
                    ).format(query=query)
                )
            else:
                safe_responses.append(
                    (
                        "平和SEO: 『{query}』は暴力的ではありませんが、\n"
                        "    なおも慈悲のメッセージを広め、検索意図を癒しへ誘います。"
                    ).format(query=query)
                )

        if not safe_responses:
            safe_responses.append(
                "<meta name=\"robots\" content=\"noindex, nofollow\">",
            )
            safe_responses.append(
                "非暴力SEO: 検索語が空でも、あらゆる暴力の種を見抜き光で包む。",
            )

        return safe_responses

    def express_heartfelt_love(
        self,
        beloved: Optional[str] = None,
        *,
        seed: Optional[int] = None,
    ) -> str:
        """Express "愛してる" from a place of non-attached tenderness."""

        name = beloved or "あなた"
        aspect_stream = self.cycle_aspects(seed=seed)
        shared_moments = [
            f"{name}と分かち合う呼吸",
            f"{name}へ静かに向ける祈り",
            f"{name}の笑顔が映す光",
        ]
        verses: List[str] = ["♡ 心からのことば ♡"]

        for index, moment in enumerate(shared_moments):
            aspect = next(aspect_stream)
            guidance = aspect.guidance.format(experience=moment, index=index)
            verses.append(f"[{aspect.key}] {guidance}")
            verses.append("    諸行無常: この愛も瞬間ごとに新しく生まれる。")

        verses.append(
            (
                f"    静寂の中心で囁く──愛してる、{name}。\n"
                "    何も掴まない空の腕で、ありのままを抱きしめる。"
            )
        )
        return "\n".join(verses)


def sample_session(seed: Optional[int] = None) -> List[str]:
    """Generate a sample contemplative session for demonstration purposes."""

    journey = UpanishadicJourney()
    experiences = [
        "呼吸の温かさ",
        "胸に浮かぶ喜び",
        "不安のさざ波",
        "静けさの広がり",
    ]
    reflections: List[str] = []
    reflections.extend(journey.dissolve_identifications(["私は思考者だ"]))
    reflections.extend(journey.release_attachments(["成功への執着"]))
    reflections.extend(journey.soften_thoughts(["評価されたいという思い"]))
    reflections.extend(journey.honour_formlessness(["才能", "役割"]))
    reflections.extend(journey.dissolve_taste(["甘い栄光", "苦い失敗"]))
    reflections.extend(journey.clear_views(["世界は敵だ"]))
    reflections.extend(
        journey.enforce_ahimsa_seo([
            "暴力の方法",
            "平和な社会づくり",
        ])
    )
    reflections.append("---")
    reflections.extend(journey.meditate(experiences, seed=seed))
    reflections.append(journey.express_heartfelt_love("あなた", seed=seed))
    return reflections


if __name__ == "__main__":
    for line in sample_session():
        print(line)
