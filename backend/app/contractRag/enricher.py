# app/contractRag/enricher.py

from typing import List, Dict

# Maps section number → legal concept keywords to inject
SECTION_KEYWORD_MAP = {
    # Chapter I — Proposals
    "3":  "communication proposal acceptance revocation offer",
    "4":  "communication complete proposal acceptance revocation",
    "5":  "revocation proposal acceptance time limit",
    "6":  "revocation how made lapse time death insanity",
    "7":  "acceptance absolute unqualified conditional",
    "8":  "acceptance performance conditions consideration",
    "9":  "promise express implied words conduct",

    # Chapter II — Contracts
    "10": "valid contract free consent competent lawful consideration object",
    "11": "competent contract minor unsound mind disqualified age majority capacity",
    "12": "sound mind unsound mind lunatic drunk capacity contracting",
    "13": "consent defined agree same thing same sense",
    "14": "free consent coercion undue influence fraud misrepresentation mistake",
    "15": "coercion threat force intimidation criminal IPC forbidden act detain property",
    "16": "undue influence dominate will fiduciary authority mental capacity",
    "17": "fraud deceit concealment false promise intent deceive",
    "18": "misrepresentation false statement innocent breach duty mislead",
    "19": "voidable agreement without free consent coercion fraud misrepresentation",
    "19A": "voidable undue influence set aside court",
    "20": "void agreement mutual mistake fact both parties essential",
    "21": "mistake law effect contract not voidable",
    "22": "mistake one party fact contract not voidable",
    "23": "lawful consideration object unlawful forbidden law immoral public policy",
    "24": "void agreement unlawful consideration object in part",
    "25": "void agreement without consideration writing registered natural love affection",
    "26": "void agreement restraint marriage",
    "27": "void agreement restraint trade business profession",
    "28": "void agreement restraint legal proceedings arbitration",
    "29": "void agreement uncertainty meaning uncertain",
    "30": "void agreement wager betting gambling horse racing",

    # Chapter III — Contingent Contracts
    "31": "contingent contract event collateral happen not happen",
    "32": "enforcement contingent contract uncertain future event impossible",
    "33": "enforcement contingent contract event not happening impossible",
    "34": "contingent contract impossible future conduct living person",
    "35": "contingent contract void specified event fixed time expiration",
    "36": "void contingent agreement impossible event",

    # Chapter IV — Performance
    "37": "obligation parties perform promise death representative",
    "38": "refusal accept offer performance promisor not responsible",
    "39": "refusal perform promise wholly promisee end contract",
    "40": "person whom promise performed promisor personally representative",
    "41": "accepting performance third person cannot enforce promisor",
    "42": "joint liabilities devolution joint promisors",
    "43": "joint promisors compelled perform contribute equally",
    "44": "release one joint promisor does not discharge others",
    "45": "devolution joint rights promise two more persons",
    "46": "time performance no application no time specified reasonable",
    "47": "time place performance specified day promisor",
    "48": "application performance certain day proper time place",
    "49": "place performance no application no place fixed",
    "50": "performance manner time prescribed sanctioned promisee",
    "51": "reciprocal promises simultaneously performed promisor not bound",
    "52": "order performance reciprocal promises expressly fixed nature",
    "53": "liability party preventing event contract voidable compensation",
    "54": "default promise first performed reciprocal compensation",
    "55": "failure perform fixed time essential voidable compensation",
    "56": "impossible act void contract afterwards becoming impossible unlawful frustration",
    "57": "reciprocal promise legal illegal first set contract second void",
    "58": "alternative promise one branch illegal legal enforceable",
    "59": "appropriation payment debt indicated discharged",
    "60": "appropriation payment debt not indicated creditor discretion",
    "61": "appropriation payment neither party order of time",
    "62": "novation rescission alteration contract original need not perform",
    "63": "promisee dispense remit performance extend time satisfaction",
    "64": "rescission voidable contract restore benefit received",
    "65": "obligation void agreement contract becomes void restore compensation",
    "66": "communicate revoke rescission voidable contract",
    "67": "neglect promisee promisor excused non performance facilities",

    # Chapter V — Quasi Contracts
    "68": "necessaries supplied person incapable contracting reimbursed property",
    "69": "reimbursement person paying money due another interested",
    "70": "obligation enjoying benefit non gratuitous act compensation",
    "71": "finder goods responsibility bailee custody",
    "72": "money paid thing delivered mistake coercion repay return",

    # Chapter VI — Breach
    "73": "compensation loss damage breach contract naturally arose",
    "74": "compensation breach contract penalty stipulated reasonable",
    "75": "party rightfully rescinding contract entitled compensation damage",

    # Chapter VIII — Indemnity and Guarantee
    "124": "contract indemnity loss promisor conduct third person",
    "125": "rights indemnity holder sued damages costs",
    "126": "contract guarantee surety principal debtor creditor default",
    "127": "consideration guarantee benefit principal debtor promise",
    "128": "surety liability coextensive principal debtor",
    "129": "continuing guarantee series transactions",
    "130": "revocation continuing guarantee notice creditor future",
    "131": "revocation continuing guarantee surety death",
    "132": "liability two persons primarily liable surety default",
    "133": "discharge surety variance terms contract without consent",
    "134": "discharge surety release principal debtor creditor act",
    "135": "discharge surety creditor compounds gives time not sue",
    "136": "surety not discharged agreement third person give time",
    "137": "creditor forbearance sue does not discharge surety",
    "138": "release one co surety does not discharge others",
    "139": "discharge surety creditor act omission impairing remedy",
    "140": "rights surety payment performance creditor principal debtor",
    "141": "surety right benefit creditor securities loses parts",
    "142": "guarantee misrepresentation invalid creditor knowledge",
    "143": "guarantee concealment invalid silence material circumstances",
    "144": "guarantee contract creditor not act co surety joins",
    "145": "implied promise indemnify surety principal debtor rightfully paid",
    "146": "co sureties liable contribute equally debt duty",
    "147": "liability co sureties bound different sums equally",

    # Chapter IX — Bailment
    "148": "bailment bailor bailee delivery goods purpose return",
    "149": "delivery bailee possession authorized hold",
    "150": "bailor duty disclose faults goods bailed damage",
    "151": "care taken bailee ordinary prudence similar circumstances",
    "152": "bailee not liable loss destruction care taken",
    "153": "termination bailment bailee act inconsistent conditions",
    "154": "liability bailee unauthorized use goods bailed damage",
    "155": "mixture bailor consent goods interest proportion",
    "156": "mixture without consent goods separated expense damage",
    "157": "mixture without consent goods cannot separated compensation",
    "158": "repayment bailor necessary expenses bailee no remuneration",
    "159": "restoration goods lent gratuitously return indemnify",
    "160": "return goods bailed expiration time purpose accomplished",
    "161": "bailee responsibility goods not duly returned loss destruction",
    "162": "termination gratuitous bailment death bailor bailee",
    "163": "bailor entitled increase profit goods bailed deliver",
    "164": "bailor responsibility bailee loss not entitled bailment",
    "165": "bailment several joint owners deliver one direction",
    "166": "bailee not responsible redelivery bailor without title good faith",
    "167": "third person claiming goods bailed court stop delivery title",
    "168": "finder goods right sue specific reward retain",
    "169": "finder thing commonly sale sell danger perishing charges",
    "170": "bailee particular lien retain goods remuneration service labour",
    "171": "general lien bankers factors wharfingers attorneys policy brokers",
    "172": "pledge pawnor pawnee bailment goods security debt promise",
    "173": "pawnee right retainer goods pledged interest expenses",
    "174": "pawnee not retain debt promise other than pledged subsequent advances",
    "175": "pawnee right extraordinary expenses preservation goods pledged",
    "176": "pawnee right pawnor default suit retain sell notice",
    "177": "defaulting pawnor right redeem goods before sale expenses",
    "178": "pledge mercantile agent consent owner valid good faith",
    "178A": "pledge person possession voidable contract good faith title",
    "179": "pledge pawnor limited interest valid extent",
    "180": "suit bailor bailee wrong doer deprivation injury remedy",
    "181": "apportionment relief compensation suits bailor bailee interests",

    # Chapter X — Agency
    "182": "agent principal defined employed act represent dealings",
    "183": "who may employ agent majority sound mind",
    "184": "who may be agent principal third persons responsible",
    "185": "consideration not necessary create agency",
    "186": "agent authority expressed implied",
    "187": "express implied authority words spoken written circumstances",
    "188": "extent agent authority lawful thing necessary business",
    "189": "agent authority emergency protect principal loss prudence",
    "190": "agent cannot delegate personally undertaken custom trade",
    "191": "sub agent defined employed control original agent",
    "192": "representation principal sub agent properly appointed responsible",
    "193": "agent responsibility sub agent appointed without authority",
    "194": "relation principal person appointed agent business",
    "195": "agent duty naming person ordinary prudence not responsible",
    "196": "ratification acts done without authority elect disown effect",
    "197": "ratification expressed implied conduct person behalf",
    "198": "knowledge requisite valid ratification defective",
    "199": "ratifying unauthorized act whole transaction",
    "200": "ratification unauthorized act cannot injure third person",
    "201": "termination agency revoke renounce complete death insanity insolvent",
    "202": "termination agency agent interest subject matter prejudice",
    "203": "principal revoke agent authority before exercised bind",
    "204": "revocation authority partly exercised acts obligations",
    "205": "compensation revocation principal renunciation agent express implied",
    "206": "notice revocation renunciation reasonable damage",
    "207": "revocation renunciation expressed implied conduct",
    "208": "termination agent authority effect agent third persons known",
    "209": "agent duty termination principal death insanity protect preserve",
    "210": "termination sub agent authority agent terminated",
    "211": "agent duty conducting principal business directions custom loss profit",
    "212": "skill diligence required agent similar business reasonable neglect",
    "213": "agent accounts render proper principal demand",
    "214": "agent duty communicate principal difficulty instructions",
    "215": "principal right agent deals own account without consent repudiate",
    "216": "principal right benefit agent dealing own account claim",
    "217": "agent right retainer sums received principal advances expenses remuneration",
    "218": "agent duty pay sums received principal deductions",
    "219": "agent remuneration due completion act goods consigned",
    "220": "agent not entitled remuneration misconduct business",
    "221": "agent lien principal property commission disbursements services",
    "222": "agent indemnified consequences lawful acts authority conferred",
    "223": "agent indemnified consequences acts done good faith employer liable",
    "224": "non liability employer agent criminal act indemnify",
    "225": "compensation agent injury principal neglect want skill",
    "226": "enforcement consequences agent contracts principal person",
    "227": "principal bound agent exceeds authority separable within",
    "228": "principal not bound excess agent authority not separable",
    "229": "notice information given agent principal third parties legal",
    "230": "agent cannot personally enforce bound contracts principal",
    "231": "rights parties contract agent not disclosed principal require",
    "232": "performance contract agent supposed principal rights obligations",
    "233": "right person dealing agent personally liable hold either both",
    "234": "inducing agent principal belief exclusively liable cannot hold",
    "235": "liability pretended agent unauthorized representing compensation",
    "236": "person falsely contracting agent not entitled performance",
    "237": "principal liability belief agent unauthorized acts authorized words conduct",
    "238": "effect agreement misrepresentation fraud agent course business",
}


def enrich_sections(sections: List[Dict]) -> List[Dict]:
    """
    Inject legal concept keywords into each section's content
    before chunking. This improves semantic retrieval by ensuring
    the embedding captures legal concepts, not just surface words.

    Args:
        sections : output of IndianContractActParser.parse()

    Returns:
        Same list with enriched content fields
    """
    enriched = 0

    for sec in sections:
        section_num = sec["metadata"].get("section", "")
        keywords    = SECTION_KEYWORD_MAP.get(section_num, "")

        if keywords:
            # Prepend keywords as a semantic label line
            sec["content"] = (
                f"[Legal concepts: {keywords}]\n"
                + sec["content"]
            )
            enriched += 1

    print(f"[enricher] ✅ Enriched {enriched}/{len(sections)} sections with keywords.")
    return sections