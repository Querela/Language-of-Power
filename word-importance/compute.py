import collections
import itertools
import logging
import os
import os.path
import pickle
import re

import numpy as np
import pandas as pd
import scipy.sparse
import sklearn.feature_extraction.text
import sklearn.linear_model
import sklearn.preprocessing
import spacy
import matplotlib.pyplot as plt
from sklearn.utils import shuffle


fn_study1_data = "Study 1/Data Study 1.xlsx"
fn_study2_data = "Study 2/Data Study 2.xlsx"

# fmt: off
COLS_LIWC_META = [
    'Dic',
]
COLS_LIWC_IGNORE = [
    'WC',
    'WPS', 'Sixltr',
]
COLS_LIWC_REL = [
    'Analytic', 'Clout', 'Authentic', 'Tone', 
    'function', 'pronoun', 'ppron', 'i', 'we', 'you_total', 'you_sing', 'you_plur', 'you_formal', 'other', 'shehe', 'they', 'ipron', 'article', 'prep', 'auxverb', 'adverb', 'conj', 'negate', 'verb', 'adj', 'compare', 'interrog', 'number', 'quant',
    'affect', 'posemo', 'negemo', 'anx', 'anger', 'sad', 'social', 'family', 'friend', 'female', 'male', 'cogproc', 'insight', 'cause', 'discrep', 'tentat', 'certain', 'differ', 'percept', 'see', 'hear', 'feel', 'bio', 'body', 'health', 'sexual', 'ingest', 'drives', 'affiliation', 'achiev', 'power', 'reward', 'risk', 'focuspast', 'focuspresent', 'focusfuture', 'relativ', 'motion', 'space', 'time', 'work', 'leisure', 'home', 'money', 'relig', 'death', 'informal', 'swear', 'netspeak', 'assent', 'nonflu', 'filler',
    'AllPunc', 'Period', 'Comma', 'Colon', 'SemiC', 'QMark', 'Exclam', 'Dash', 'Quote', 'Apostro', 'Parenth', 'OtherP',
]
COLS_LIWC_ALL = COLS_LIWC_META + COLS_LIWC_IGNORE + COLS_LIWC_REL

COL_TEXT = "text"
COL_TEXT_SPACY = "text_spacy_doc"
COL_TEXT_SPACY_CLEAN = "text_spacy_doc_filtered"

COLS_SCORES = [
    "s:power",
    "s:dominance",
    "s:prestige",
    "s:power_f",
    "s:dominance_f",
    "s:prestige_f",
]
COLS_SCORES_S2 = [
    "s:workplace_power",
    "s:workplace_power_f",
]
COLS_SCORES_ALL = COLS_SCORES + COLS_SCORES_S2
# fmt: on


LOGGER = logging.getLogger(__name__)


# --------------------------------------------------------------------------


def load_study1(fn_data=fn_study1_data, load_text=True, load_meta=True, load_metrics=True, load_liwc=True):
    df_study1 = pd.read_excel(fn_data)

    cols = [
        # id
        "ID",
    ]
    col_renames = dict()
    if load_text:
        cols += [
            # raw text
            "SourceB",
        ]
        col_renames.update({
            "SourceB": COL_TEXT,
        })
    if load_meta:
        cols += [
            # other meta
            "Alter",
            "Geschlecht",
        ]
        col_renames.update({
            "Alter": "age",
            "Geschlecht": "gender",
        })
    if load_metrics:
        cols += [
            # self-evaluation (mean)
            "Power_mean",
            "Dom_mean",
            "Pres_mean",
            # outside-evaluation (mean)
            "Power_F",
            "Dom_F",
            "Pres_F",
        ]
        col_renames.update({
            "Power_mean": "s:power",
            "Dom_mean": "s:dominance",
            "Pres_mean": "s:prestige",
            "Power_F": "s:power_f",
            "Dom_F": "s:dominance_f",
            "Pres_F": "s:prestige_f",
        })
    if load_liwc:
        cols += COLS_LIWC_ALL

    # just keep useful columns
    df_study1 = df_study1[cols]

    # rename columns
    df_study1.rename(columns=col_renames, inplace=True)

    return df_study1


def load_study2(fn_data=fn_study2_data, load_text=True, load_meta=True, load_metrics=True, load_liwc=True):
    df_study2 = pd.read_excel(fn_data)

    cols = [
        # id
        "ID",
    ]
    col_renames = dict()
    if load_text:
        cols += [
            # raw text
            "SourceA",
        ]
        col_renames.update({
            "SourceA": COL_TEXT,
        })
    if load_meta:
        cols += [
            # other meta
            "Alter",
            "Geschlecht",
        ]
        col_renames.update({
            "Alter": "age",
            "Geschlecht": "gender",
        })
    if load_metrics:
        cols += [
            # self-evaluation (mean)
            "Power_means",
            "Dominanz_means",
            "Prestige_means",
            # outside-evaluation (mean)
            "Power_Fremdgesamt_means",
            "Dominanz_Fremdgesamt_means",
            "Prestige_Fremdgesamt_means",
            # WP (workplace power)?
            "WP_means",
            "WP_Fremdgesamt_means",
        ]
        col_renames.update({
            "Power_means": "s:power",
            "Dominanz_means": "s:dominance",
            "Prestige_means": "s:prestige",
            "Power_Fremdgesamt_means": "s:power_f",
            "Dominanz_Fremdgesamt_means": "s:dominance_f",
            "Prestige_Fremdgesamt_means": "s:prestige_f",
            "WP_means": "s:workplace_power",
            "WP_Fremdgesamt_means": "s:workplace_power_f",
        })
    if load_liwc:
        cols += COLS_LIWC_ALL

    # just keep useful columns
    df_study2 = df_study2[cols]

    # rename columns
    df_study2.rename(columns=col_renames, inplace=True)

    return df_study2


# --------------------------------------------------------------------------


def nlpize(df, nlp_fn):
    return df.map(nlp_fn)


# --------------------------------------------------------------------------


def clean(df, stopwords=False, alpha=False, punctuation=True):
    # filter out stopwords
    if stopwords:
        df = df.map(lambda doc: list(filter(lambda tok: not tok.is_stop, doc)))

    # filter alphanumerical
    if alpha:
        df = df.map(lambda doc: list(filter(lambda tok: tok.is_alpha, doc)))

    # filter out punctuation
    if punctuation:
        df = df.map(
            lambda doc: list(filter(lambda tok: tok.pos_ not in ("PUNCT"), doc))
        )

    # filter out space
    df = df.map(lambda doc: list(filter(lambda tok: not tok.is_space, doc)))

    return df


def remove_punct(df):
    return df.map(lambda x: re.sub(r"[,\.!?]", "", x))


def lowercase_text(df):
    return df.map(lambda x: x.lower())


def get_text_by_pos(df, pos_list=("NOUN",), lemma=False, join=True):
    # filter each token by correct pos tag
    if pos_list:
        df = df.map(lambda x: list(filter(lambda tok: tok.pos_ in pos_list, x)))

    # convert tokens back to strings
    # df = df.map(lambda x: " ".join(map(str, x)))
    if lemma:
        df = df.map(lambda x: " ".join(map(lambda tok: tok.lemma_, x)))
    else:
        df = df.map(lambda x: " ".join(map(lambda tok: tok.text, x)))

    # concat to single text
    if not join:
        return df

    return " ".join(df.values.tolist())


def get_tokens_by_pos(df, pos_list=("NOUN",), lemma=False, join=True):
    # filter each token by correct pos tag
    if pos_list:
        df = df.map(lambda x: list(filter(lambda tok: tok.pos_ in pos_list, x)))

    # convert tokens back to strings
    # df = df.map(lambda x: " ".join(map(str, x)))
    if lemma:
        df = df.map(lambda x: list(map(lambda tok: tok.lemma_, x)))
    else:
        df = df.map(lambda x: list(map(lambda tok: tok.text, x)))

    # concat to single text
    if not join:
        return df

    return list(itertools.chain(*df.values.tolist()))


# --------------------------------------------------------------------------


def prepare_study_data():
    LOGGER.info("Load study data ...")
    df_study1 = load_study1()
    df_study2 = load_study2()

    # --------------------------------------------------
    LOGGER.info("Run spaCy on data ...")
    # import de_core_news_sm
    # import de_dep_news_trf
    # nlp = de_core_news_sm.load()
    # nlp = de_dep_news_trf.load()

    # nlp = spacy.load("de_core_news_sm")
    nlp = spacy.load("de_dep_news_trf")

    df_study1[COL_TEXT_SPACY] = nlpize(df_study1[COL_TEXT], nlp)
    df_study2[COL_TEXT_SPACY] = nlpize(df_study2[COL_TEXT], nlp)

    # --------------------------------------------------
    return df_study1, df_study2


def clean_study_data(
    df_study1, df_study2, do_clean_stopwords=True, do_clean_alpha=True
):
    LOGGER.info("Clean study data ...")
    df_study1[COL_TEXT_SPACY_CLEAN] = clean(
        df_study1[COL_TEXT_SPACY],
        stopwords=do_clean_stopwords,
        alpha=do_clean_alpha,
        punctuation=True,
    )
    df_study2[COL_TEXT_SPACY_CLEAN] = clean(
        df_study2[COL_TEXT_SPACY],
        stopwords=do_clean_stopwords,
        alpha=do_clean_alpha,
        punctuation=True,
    )

    # take raw text `tok.text` instead of lemma `tok.lemma_`
    # df_study1["tokens"] = df_study1[COL_TEXT_SPACY_CLEAN].map(lambda doc: list(map(lambda tok: tok.text, doc)))
    # df_study2["tokens"] = df_study2[COL_TEXT_SPACY_CLEAN].map(lambda doc: list(map(lambda tok: tok.text, doc)))
    # convert to plain string
    # df_study1["tokens"] = df_study1["tokens"].map(lambda doc: list(map(str, doc)))
    # df_study2["tokens"] = df_study2["tokens"].map(lambda doc: list(map(str, doc)))

    # Remove punctuation
    # df_study1["text_processed"] = remove_punct(df_study1[COL_TEXT])
    # df_study2["text_processed"] = remove_punct(df_study2[COL_TEXT])
    # Convert the titles to lowercase
    # df_study1['text_processed'] = lowercase_text(df_study1['text_processed'])
    # df_study2['text_processed'] = lowercase_text(df_study2['text_processed'])

    # --------------------------------------------------
    return df_study1, df_study2


def load_cached_data(
    fn_study_prepared="studydata.pickle", do_clean_stopwords=True, do_clean_alpha=True
):
    if not os.path.exists(fn_study_prepared):
        df_study1, df_study2 = prepare_study_data()

        with open(fn_study_prepared, "wb") as fp:
            pickle.dump(df_study1, fp, protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(df_study2, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open(fn_study_prepared, "rb") as fp:
        df_study1 = pickle.load(fp)
        df_study2 = pickle.load(fp)

    df_study1, df_study2 = clean_study_data(
        df_study1,
        df_study2,
        do_clean_stopwords=do_clean_stopwords,
        do_clean_alpha=do_clean_alpha,
    )

    return df_study1, df_study2


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


def make_word_freqs_for_top_N(df, N=None, weights_original=False):
    # count number of tokens
    def _token_freqs_fn(doc):
        cnt = collections.Counter(doc)
        num_tokens = sum(cnt.values())
        return {word: num / num_tokens for word, num in cnt.items()}

    df_freqs = df.map(_token_freqs_fn)

    if N is None:
        return df_freqs

    # --------------------------------------------------

    # get N-most frequently occuring words (based on relative counts)
    df_freqs_all = collections.Counter()
    for doc in df_freqs.values.tolist():
        df_freqs_all.update(doc)

    # # set cutoff
    # if N is None:
    #     N = len(df_freqs_all)

    types_top_N = df_freqs_all.most_common(N)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            "Top-10 Types: %s",
            ", ".join("{} ({:.2f})".format(w, c) for w, c in types_top_N[:10]),
        )
        LOGGER.debug(
            "Bottom-10 Types: %s",
            ", ".join("{} ({:.2f})".format(w, c) for w, c in types_top_N[-10:]),
        )
    types_top_N = dict(types_top_N)

    # filter out types in documents that are not in top-N
    types_to_keep = set(types_top_N.keys())

    if weights_original:
        # if we do not want to update the total token count, then we can just return here
        def _filter_tokens_fn(doc):
            return {k: v for k, v in doc.items() if k in types_to_keep}

        return df_freqs.map(_filter_tokens_fn)

    # --------------------------------------------------

    # get updated token weights --> since total token count changed, recompute
    def _token_freqs_fn(doc):
        cnt = collections.Counter(doc)
        cnt = {k: v for k, v in cnt.items() if k in types_to_keep}
        num_tokens = sum(cnt.values())
        return {word: num / num_tokens for word, num in cnt.items()}

    df_freqs = df.map(_token_freqs_fn)

    if LOGGER.isEnabledFor(logging.DEBUG):
        df_freqs_all = collections.Counter()
        for doc in df_freqs.values.tolist():
            df_freqs_all.update(doc)

        types_top_N = df_freqs_all.most_common(N)
        LOGGER.debug(
            "Top-10 Types: %s",
            ", ".join("{} ({:.2f})".format(w, c) for w, c in types_top_N[:10]),
        )
        LOGGER.debug(
            "Bottom-10 Types: %s",
            ", ".join("{} ({:.2f})".format(w, c) for w, c in types_top_N[-10:]),
        )

    return df_freqs


# --------------------------------------------------------------------------


def _get_ranks(df):
    types = collections.Counter()
    for doc in df.values.tolist():
        types.update(doc)
    ordered = types.most_common()
    return {word: rank for rank, (word, _) in enumerate(ordered, 1)}


def make_token_rank_split_halves(df_freqs, types=None, random_state=None):
    if types is None:
        # generate list of all types (ordered descending)
        types = collections.Counter()
        for doc in df_freqs.values.tolist():
            types.update(doc)
        types = dict(types.most_common())

    idx_shuffled = shuffle(df_freqs.index.values, random_state=random_state)
    df_tok_a = df_freqs[idx_shuffled[: len(idx_shuffled) // 2]]
    df_tok_b = df_freqs[idx_shuffled[len(idx_shuffled) // 2 :]]

    ranks_a = _get_ranks(df_tok_a)
    ranks_b = _get_ranks(df_tok_b)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            "Ranks (half/a): %s", ", ".join(w for w, _ in list(ranks_a.items())[:10])
        )
        LOGGER.debug(
            "Ranks (half/b): %s", ", ".join(w for w, _ in list(ranks_b.items())[:10])
        )

    types = list(types.keys())
    ranklist_a = np.array([ranks_a.get(word, None) for word in types], dtype=float)
    ranklist_b = np.array([ranks_b.get(word, None) for word in types], dtype=float)

    return ranklist_a, ranklist_b, types


def generate_token_rank_correlation_plot(
    df_study, dn_output="figures", N=None, random_state=None
):
    os.makedirs(dn_output, exist_ok=True)

    df_docs = df_study[COL_TEXT_SPACY_CLEAN]
    df_tokens = get_tokens_by_pos(df_docs, pos_list=None, lemma=False, join=False)
    df_freqs = make_word_freqs_for_top_N(df_tokens, N=N)
    ranklist_a, ranklist_b, types = make_token_rank_split_halves(
        df_freqs, random_state=random_state
    )
    print(ranklist_a)
    print(ranklist_b)

    N = N if N is not None else len(types)
    ranks = np.arange(1, N)
    corrs = np.array(
        [
            scipy.stats.spearmanr(
                ranklist_a[:cutoff], ranklist_b[:cutoff], nan_policy="omit"
            ).correlation
            for cutoff in ranks
        ]
    )

    # TODO: smoothing?
    # from scipy.signal import savgol_filter
    # corrshat = savgol_filter(corrs, 41, 1) # window size 51, polynomial order 1

    plt.plot(ranks, corrs)
    # plt.plot(ranks, corrshat)
    plt.title("Correlation at Rank")
    plt.ylabel("Corrleation")
    plt.xlabel("Rank")
    plt.ylim((0, 1))
    plt.savefig(
        os.path.join(dn_output, "token_rank_correlation.png"), bbox_inches="tight"
    )
    plt.close()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


def make_word_freq_df(
    df,
    by="power",
    pos=("NOUN", "PROPN"),
    lemma=True,
    max_freq=None,
    min_freq=10,
    relative=False,
):
    row = df[by].map(round)

    dfs_score = []
    for score in range(1, 8):  # range: [1, 7]
        mask = row == score
        df_sub = df[mask][COL_TEXT_SPACY_CLEAN]
        tokens = get_tokens_by_pos(df_sub, pos_list=pos, lemma=lemma, join=True)
        cnt = collections.Counter(tokens)

        df_score = pd.DataFrame.from_dict(cnt, orient="index").rename(
            columns={0: f"{by}={score}"}
        )
        dfs_score.append(df_score)

    df_scores = pd.concat(dfs_score, axis=1).fillna(0)
    df_scores["_total"] = df_scores.sum(axis=1)
    df_scores = df_scores.sort_values("_total", ascending=False)
    if max_freq is not None:
        df_scores = df_scores[df_scores["_total"] <= max_freq]
    if min_freq is not None:
        df_scores = df_scores[df_scores["_total"] >= min_freq]
    del df_scores["_total"]

    if relative:
        totals = df_scores.sum(axis=0)
        df_scores /= totals

    return df_scores


def make_word_freq_score_comparison_df(
    df,
    parts,
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=None,
):
    dfs_cnts = []
    for mask, name in parts:
        df_sub = df[mask][COL_TEXT_SPACY_CLEAN]
        tokens_low = get_tokens_by_pos(df_sub, pos_list=pos, lemma=lemma, join=True)
        cnt = collections.Counter(tokens_low)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                "Top words: %s",
                "".join(
                    ["{} ({})".format(w, n) for w, n in cnt.most_common(10) if n > 1]
                ),
            )
        df_cnt = pd.DataFrame.from_dict(cnt, orient="index").rename(
            columns={0: name}
        )  # .reset_index()
        dfs_cnts.append(df_cnt)

    df_lmh = pd.concat(dfs_cnts, axis=1).fillna(0)
    df_lmh["_total"] = df_lmh.sum(axis=1)
    df_lmh = df_lmh.sort_values("_total", ascending=False)
    df_lmh = df_lmh[df_lmh["_total"] >= total_occ_min]
    del df_lmh["_total"]

    # restrict to max N entries
    if max_rows is not None and max_rows > 0:
        df_lmh = df_lmh.head(max_rows)

    if relative:
        # make relative
        totals = df_lmh.sum(axis=0)
        df_lmh /= totals

    return df_lmh


def make_word_freq_score_lmh_comparison_df(
    df,
    what,
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=20,
):
    parts = list(zip(get_lmh_quantiles_mask(df, what), ["low", "mid", "high"]))

    return make_word_freq_score_comparison_df(
        df,
        parts,
        pos=pos,
        lemma=lemma,
        relative=relative,
        total_occ_min=total_occ_min,
        max_rows=max_rows,
    )


def make_word_freq_score_pdp_comparison_df(
    df,
    whats=("power", "dominance", "prestige"),
    range_=(2 / 3, 1.0),
    pos=("NOUN", "PROPN"),
    lemma=True,
    relative=False,
    total_occ_min=10,
    max_rows=20,
):
    parts = []
    for what in whats:
        q1, q2 = df[what].quantile(range_)
        if range_[0] <= 0.0:
            mask = df[what] <= q2
        elif range_[1] >= 1.0:
            mask = df[what] > q1
        else:
            mask = (df[what] > q1) & (df[what] <= q2)
        parts.append([mask, what.title()])

    return make_word_freq_score_comparison_df(
        df,
        parts,
        pos=pos,
        lemma=lemma,
        relative=relative,
        total_occ_min=total_occ_min,
        max_rows=max_rows,
    )


def get_lmh_quantiles_mask(df, what):
    q33 = df[what].quantile(1 / 3)
    q66 = df[what].quantile(2 / 3)

    mask_low = df[what] <= q33
    mask_mid = (df[what] > q33) & (df[what] <= q66)
    mask_high = df[what] > q66

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug("quant(%s): low: %s", what, len(df[mask_low]))
        LOGGER.debug("quant(%s): mid: %s", what, len(df[mask_mid]))
        LOGGER.debug("quant(%s): high: %s", what, len(df[mask_high]))

    return mask_low, mask_mid, mask_high


# --------------------------------------------------------------------------


def write_freqs_to_excel(
    df_study, fn_output="output.xlsx", lemma=True, relative=False, total_occ_min=3
):
    with pd.ExcelWriter(fn_output) as writer:
        df_study_t = df_study.copy()
        df_study_t = df_study_t[list(set(df_study.columns) - {"text_spacy_doc"})]
        df_study_t[COL_TEXT_SPACY_CLEAN] = df_study_t[
            "text_spacy_doc_filtered"
        ].map(lambda x: ", ".join(map(lambda tok: tok.text, x)))
        df_study_t.to_excel(writer, sheet_name="Study Data")

        pdp = ["power", "dominance", "prestige"]
        pdpf = ["power_f", "dominance_f", "prestige_f"]
        if "workplace_power" in df_study.columns:
            pdp += ["workplace_power"]
            pdpf += ["workplace_power_f"]

        df_study_quants = df_study[pdp + pdpf].quantile([0 / 3, 1 / 3, 2 / 3, 3 / 3])
        df_study_quants.to_excel(writer, sheet_name="Quantiles")

        # by trait, for POS tags, per low/mid/high
        poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
        for pos in poss:
            for what in pdp:
                df_lmh = make_word_freq_score_lmh_comparison_df(
                    df_study,
                    what,
                    pos=pos,
                    lemma=lemma,
                    relative=relative,
                    total_occ_min=total_occ_min,
                )
                title = "Words for '{}' for {}".format(
                    what.replace("workplace_power", "WrkPow")
                    .replace("dominance", "Dom")
                    .title(),
                    ", ".join(pos),
                )
                df_lmh.to_excel(writer, sheet_name=title[10:].replace("'", ""))

        # by quantil range + per category/dimension/trait
        poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
        ranges = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
        whatss = [pdp, pdpf, *zip(pdp, pdpf)]
        for pos in poss:
            for range_ in ranges:
                for wi, whats in enumerate(whatss):
                    df_h_pdp = make_word_freq_score_pdp_comparison_df(
                        df_study,
                        whats=whats,
                        range_=range_,
                        pos=pos,
                        lemma=lemma,
                        relative=relative,
                        total_occ_min=total_occ_min,
                    )
                    title = "Words for quantile {:.2f}-{:.2f} for {}".format(
                        *range_, ", ".join(pos)
                    )
                    title = "Qnt {:.1f}-{:.1f} for {} {}".format(
                        *range_, ",".join(pos), wi
                    )
                    df_h_pdp.to_excel(writer, sheet_name=title)


def generate_freqs_figures(
    df_study,
    dn_output="figures",
    lemma=True,
    relative=True,
    total_occ_min=10,
    max_rows=20,
    plot_type="barh",
):
    os.makedirs(dn_output, exist_ok=True)
    os.makedirs(os.path.join(dn_output, "distribution"), exist_ok=True)
    os.makedirs(os.path.join(dn_output, "mid-low-high"), exist_ok=True)
    os.makedirs(os.path.join(dn_output, "comparison"), exist_ok=True)

    pdp = ["power", "dominance", "prestige"]
    pdpf = ["power_f", "dominance_f", "prestige_f"]
    if "workplace_power" in df_study.columns:
        pdp += ["workplace_power"]
        pdpf += ["workplace_power_f"]

    for what in pdp + pdpf:
        df_study[what].hist()
        min_ylim, max_ylim = plt.ylim()
        q33 = df_study[what].quantile(1 / 3)
        q66 = df_study[what].quantile(2 / 3)
        plt.axvline(q33, color="k", linestyle="dashed", linewidth=1)
        plt.text(q33 * 1.01, max_ylim * 0.9, "{:.2f}".format(q33))
        plt.axvline(q66, color="k", linestyle="dashed", linewidth=1)
        plt.text(q66 * 1.01, max_ylim * 0.9, "{:.2f}".format(q66))
        plt.savefig(
            os.path.join(
                dn_output, "distribution", "quant-{}.png".format(what.lower())
            ),
            bbox_inches="tight",
        )
        plt.close()

    # by trait, for POS tags, per low/mid/high
    poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
    for pos in poss:
        for what in pdp:
            local_total_occ_min = total_occ_min
            if pos in (("ADJ",),):
                local_total_occ_min = 3
            df_lmh = make_word_freq_score_lmh_comparison_df(
                df_study,
                what,
                pos=pos,
                lemma=lemma,
                relative=relative,
                total_occ_min=local_total_occ_min,
                max_rows=max_rows,
            )
            title = "Words for '{}' for {}".format(what.title(), ", ".join(pos))
            df_lmh.plot(kind=plot_type)
            plt.title(title)
            plt.savefig(
                os.path.join(
                    dn_output,
                    "mid-low-high",
                    "words-{}-by-pos-{}.png".format(what.lower(), ",".join(pos)),
                ),
                bbox_inches="tight",
            )
            plt.close()

    # by quantil range + per category/dimension/trait
    poss = [("NOUN", "PROPN"), ("ADJ",), ("ADV",), ("VERB",)]
    ranges = [(0.0, 1 / 3), (1 / 3, 2 / 3), (2 / 3, 1.0)]
    whatss = [pdp, pdpf, *zip(pdp, pdpf)]
    for pos in poss:
        for range_ in ranges:
            for whats in whatss:
                local_total_occ_min = total_occ_min
                if pos in (("ADJ",),):
                    local_total_occ_min = 3
                df_h_pdp = make_word_freq_score_pdp_comparison_df(
                    df_study,
                    whats=whats,
                    range_=range_,
                    pos=pos,
                    lemma=lemma,
                    relative=relative,
                    total_occ_min=local_total_occ_min,
                    max_rows=max_rows,
                )
                title = "Words for quantile {:.2f}-{:.2f} for {}".format(
                    *range_, ", ".join(pos)
                )
                df_h_pdp.plot(kind=plot_type)
                plt.title(title)
                plt.savefig(
                    os.path.join(
                        dn_output,
                        "comparison",
                        "words-by-quant-{:.1f}-{:.1f}+pos-{}-for-{}.png".format(
                            *range_, ",".join(pos), ",".join(whats)
                        ),
                    ),
                    bbox_inches="tight",
                )
                plt.close()


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------


def build_count_matrix(df, pos_list=None, lemma=False):
    # tokens
    df_tokens = get_tokens_by_pos(df, pos_list=pos_list, lemma=lemma, join=False)
    # token counts
    df_tokens_cnt = df_tokens.map(lambda x: collections.Counter(x))
    # aggregate count --> features
    cnt_tokens = collections.Counter()
    df_tokens_cnt.map(cnt_tokens.update)

    # features
    features = list(cnt_tokens.keys())

    # build sparse features matrix (document, term)
    indptr = [0]
    indices = []
    values = []
    for row in df_tokens_cnt:
        for term, num in row.items():
            indices.append(features.index(term))
            values.append(num)
        indptr.append(len(indices))

    doc_term_mat = scipy.sparse.csr_array((values, indices, indptr), dtype=int)
    # for sklearn `features_names_in_`
    doc_term_mat.columns = features

    return doc_term_mat, features


def build_feature_matrix(df, pos_list=None, lemma=False, norm="l1", use_idf=False):
    transformer = sklearn.feature_extraction.text.TfidfTransformer(
        norm=norm, use_idf=use_idf
    )

    doc_term_mat, features = build_count_matrix(df, pos_list=pos_list, lemma=lemma)

    doc_term_mat = transformer.fit_transform(doc_term_mat.toarray())
    # for sklearn `features_names_in_`
    doc_term_mat.columns = features

    return doc_term_mat, features


# --------------------------------------------------------------------------


def train_prepare(df_study, pos_list=None, lemma=False):
    df_sub = df_study[COL_TEXT_SPACY_CLEAN]
    # doc_term_mat, features = build_count_matrix(df_sub, pos_list=pos_list, lemma=lemma)
    doc_term_mat, features = build_feature_matrix(
        df_sub, pos_list=pos_list, lemma=lemma, norm="l2", use_idf=True
    )

    return doc_term_mat


def train_model(df_study, what, doc_term_mat):
    # if doc_term_mat is None:
    #     doc_term_mat = train_prepare(df_study)

    clf = sklearn.linear_model.LogisticRegression()

    X = doc_term_mat
    y = df_study[what].to_numpy()

    # classification
    # y = y.astype(int)
    # y = np.vectorize(round)(y)
    y = y.round()

    # regression: to interval [0, 1]
    # y = (y - np.min(y)) / np.ptp(y)
    # y = y[:,np.newaxis]

    # train model
    clf.fit(X, y)
    LOGGER.info("score (on train): %s (for '%s')", clf.score(X, y), what)

    return clf


def coef_aggregate(coefs, num_classes):
    coefs = coefs * np.linspace(-1, 1, num_classes)[:, np.newaxis]
    return coefs.sum(axis=0)


def normalize_coefs(coefs, neg_coefs=True):
    if neg_coefs:
        # norm: [-1, 1]
        coefs = 2.0 * (coefs - np.min(coefs)) / np.ptp(coefs) - 1
    else:
        # norm: [0, 1]
        coefs = (coefs - np.min(coefs)) / np.ptp(coefs)

    return coefs


def coef_filter(coef, features, min_threshold=0.25, max_features=20, require_both=True):
    if require_both:
        # try to request from both ends to keep pos and neg (min/max)
        mask = np.zeros_like(coef).astype(bool)
        mask[: max_features // 2 + 1] = mask[-max_features // 2 :] = True

        srt = np.argsort(coef)[::-1]
        # pre-filter features
        features = np.array(features)[srt][mask]
        coef = np.array(coef)[srt][mask]

    # sort by importance (most positive/negative first)
    srt = np.argsort(np.abs(coef))[::-1]
    # minimum importance filter
    mask = np.abs(coef) >= min_threshold
    mask_srt = mask[srt]
    # max feature filter
    mask_srt[max_features:] = False
    # filter features
    labels_srt = np.array(features)[srt][mask_srt]
    values_srt = np.array(coef)[srt][mask_srt]

    # sort by value descending
    srt = np.argsort(values_srt)[::-1]
    labels = labels_srt[srt]
    values = values_srt[srt]

    return values, labels


def coef_to_human(values, labels):
    return " + ".join(
        "{:.2f}*'{}'".format(value, label) for label, value in zip(labels, values)
    )


# --------------------------------------------------------------------------


def write_coefs_to_excel(
    clf,
    what,
    fn_output="coefs.xlsx",
    min_threshold=0.20,
    max_features=30,
    require_both=False,
):
    skip = 4
    features = clf.feature_names_in_
    coefs = clf.coef_.copy()
    coefs = normalize_coefs(coefs)

    mode = "a" if os.path.exists(fn_output) else "w"
    ise = "overlay" if os.path.exists(fn_output) else None
    with pd.ExcelWriter(fn_output, mode=mode, if_sheet_exists=ise) as writer:
        # per class coefs
        for ci, (class_, coef) in enumerate(zip(clf.classes_, coefs)):
            values, labels = coef_filter(
                coef,
                features,
                min_threshold=min_threshold,
                max_features=max_features,
                require_both=require_both,
            )
            col_lbl = "Class {:d}".format(int(class_))
            cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
            df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
            df_coef.to_excel(
                writer, sheet_name="{}".format(what.title()), startcol=ci * skip
            )

        ci += 1
        # aggregated coefs
        coefs = clf.coef_.copy()
        coefs = coefs * np.linspace(-1, 1, len(clf.classes_))[:, np.newaxis]
        coefs = coefs.sum(axis=0)
        coefs = normalize_coefs(coefs)
        values, labels = coef_filter(
            coefs,
            features,
            min_threshold=min_threshold,
            max_features=max_features,
            require_both=require_both,
        )
        col_lbl = "Aggregated"
        cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
        df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
        df_coef.to_excel(
            writer, sheet_name="{}".format(what.title()), startcol=ci * skip
        )

        # averaged coedfs
        # should not make sense as we then have equal contributions from both low and high power for example
        # ci += 1
        # coefs = clf.coef_.copy()
        # coefs = coefs.mean(axis=0)
        # coefs = normalize_coefs(coefs)
        # values, labels = coef_filter(coefs, features, min_threshold=min_threshold, max_features=max_features, require_both=require_both)
        # col_lbl = "Averaged"
        # cols = pd.MultiIndex.from_tuples([(col_lbl, "words"), (col_lbl, "coefs")])
        # df_coef = pd.DataFrame.from_records(data=zip(labels, values), columns=cols)
        # df_coef.to_excel(writer, sheet_name="{}".format(what.title()), startcol=ci*3)


def train_and_write_coefs_to_excel(
    df_study,
    fn_output="coefs.xlsx",
    pos_list=None,
    lemma=False,
    min_threshold=0.20,
    max_features=30,
    require_both=True,
):
    pdp = ["power", "dominance", "prestige"]
    pdpf = ["power_f", "dominance_f", "prestige_f"]
    if "workplace_power" in df_study.columns:
        pdp += ["workplace_power"]
        pdpf += ["workplace_power_f"]

    doc_term_mat = train_prepare(df_study, pos_list=pos_list, lemma=lemma)
    for what in pdp + pdpf:
        clf = train_model(df_study, what, doc_term_mat=doc_term_mat)
        write_coefs_to_excel(
            clf,
            what,
            fn_output=fn_output,
            min_threshold=min_threshold,
            max_features=max_features,
            require_both=require_both,
        )


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


def compute_category_word_correlation(
    df_study,
    hier_var_cols,
    doc_col="text_spacy_doc_filtered",
    pos_list=None,
    lemma=False,
    tfidf=False,
):
    # scores
    df_scores = df_study[hier_var_cols]

    # preprocessed documents (spacy tokenized, some filtering of non-words)
    df_documents = df_study[doc_col]

    # --------------------------------------------------

    # build a feature matrix (relative word frequency per document)
    kwargs = dict(norm="l2", use_idf=True) if tfidf else dict()
    mat, words = build_feature_matrix(
        df_documents, pos_list=pos_list, lemma=lemma, **kwargs
    )
    df_features = pd.DataFrame(mat.todense())
    df_features.columns = words

    # add prefix, just to be sure not to have overlaps
    col_prefix = "hierarchy_variables:"
    df_scores_prefixed = df_scores.add_prefix(col_prefix)
    hier_var_cols_prefixed = ["{}{}".format(col_prefix, col) for col in hier_var_cols]

    # add hierarchy variables
    df_features = pd.merge(
        df_features, df_scores_prefixed, left_index=True, right_index=True
    )

    # correlate
    df_corrs = df_features.corr()

    # just keep hierarchy variable colums
    # (correlation hierarchy variable to words, based on score)
    df_corrs = df_corrs[hier_var_cols_prefixed]

    # remove correlation
    df_corrs = df_corrs.drop(hier_var_cols_prefixed)

    df_corrs = df_corrs.rename(columns=dict(zip(hier_var_cols_prefixed, hier_var_cols)))

    return df_corrs


def filter_category_word_correlations(
    df_corrs, hier_var_cols, topn=20, require_both=True
):
    topn_half = topn // 2
    if topn % 2 == 1:
        topn_half += 1

    # only filter out those per variable with N highest absolute values
    mask = np.zeros_like(df_corrs.index).astype(bool)
    for col in hier_var_cols:
        if require_both:
            srt = np.argsort(df_corrs[col])[::-1]
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(
                    "Pos-Top-%s of '%s': %s",
                    topn_half,
                    col,
                    ", ".join(
                        "{} ({:.2f})".format(w, v)
                        for w, v in df_corrs[col][srt][:topn_half].to_dict().items()
                    ),
                )
                LOGGER.debug(
                    "Neg-Top-%s of '%s': %s",
                    topn_half,
                    col,
                    ", ".join(
                        "{} ({:.2f})".format(w, v)
                        for w, v in df_corrs[col][srt][-topn_half:].to_dict().items()
                    ),
                )
            mask[srt[:topn_half]] = True
            mask[srt[-topn_half:]] = True
        else:
            srt = np.argsort(df_corrs[col].abs())[::-1]
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug(
                    "Top-%s of '%s': %s",
                    topn,
                    col,
                    ", ".join(
                        "{} ({:.2f})".format(w, v)
                        for w, v in df_corrs[col][srt][:topn].to_dict().items()
                    ),
                )
            mask[srt[:topn]] = True

    mask = pd.Series(mask, index=df_corrs.index)
    return df_corrs[mask]


def compute_and_write_category_word_correlation_to_excel(
    df_study,
    fn_output="corrs.xlsx",
    doc_col="text_spacy_doc_filtered",
    pos_list=None,
    lemma=False,
    tfidf=False,
    topn=20,
    require_both=True,
    color=True,
):
    # hierarchy variables (score) columns
    pdp = ["power", "dominance", "prestige"]
    pdpf = ["power_f", "dominance_f", "prestige_f"]
    if "workplace_power" in df_study.columns:
        pdp += ["workplace_power"]
        pdpf += ["workplace_power_f"]

    hier_var_cols = pdp + pdpf

    df_corrs = compute_category_word_correlation(
        df_study,
        hier_var_cols,
        doc_col=doc_col,
        pos_list=pos_list,
        lemma=lemma,
        tfidf=tfidf,
    )

    if os.path.exists(fn_output):
        os.unlink(fn_output)

    mode = "a" if os.path.exists(fn_output) else "w"
    ise = "overlay" if os.path.exists(fn_output) else None
    with pd.ExcelWriter(fn_output, mode=mode, if_sheet_exists=ise) as writer:

        def _highlight_top_both(col, topn, props=""):
            topn_half = topn // 2 + (1 if topn % 2 == 1 else 0)

            return pd.Series(
                props,
                index=np.concatenate(
                    [
                        col.index[np.argsort(col)[::-1]][:topn_half],
                        col.index[np.argsort(col)[::-1]][-topn_half:],
                    ]
                ),
            )

        def _highlight_top(col, topn, props=""):
            return pd.Series(props, index=col.index[np.argsort(col.abs())[::-1]][:topn])

        if color:
            df_corrs.style.apply(
                _highlight_top_both if require_both else _highlight_top,
                topn=topn,
                props="font-weight:bold;",
                axis=0,
            ).text_gradient(axis=0).to_excel(writer, sheet_name="Correlations (all)")
        else:
            df_corrs.to_excel(writer, sheet_name="Correlations (all)")

        df_corrs_sub = filter_category_word_correlations(
            df_corrs, hier_var_cols, topn=topn, require_both=require_both
        )

        if color:
            df_corrs_sub = df_corrs_sub.style.apply(
                _highlight_top_both if require_both else _highlight_top,
                topn=topn,
                props="font-weight:bold;",
                axis=0,
            )

        df_corrs_sub.to_excel(writer, sheet_name=f"Correlations (Top-{topn})")

        for col in hier_var_cols:
            df_corrs_sub = filter_category_word_correlations(
                df_corrs[[col]], [col], topn=topn, require_both=require_both
            )
            df_corrs_sub = df_corrs_sub.sort_values(
                by=[col],
                ascending=False,
                # if sorted by "magnitude" (not just by value)
                # key=lambda col: col.abs()
            )
            if color:
                df_corrs_sub = df_corrs_sub.style.text_gradient(axis=0, cmap="RdYlGn")
            df_corrs_sub.to_excel(writer, sheet_name=f"{col} {topn}")


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s"
    )
    LOGGER.info("Run as script ...")

    LOGGER.info("Load data ...")
    df_study1, df_study2 = load_cached_data(do_clean_stopwords=True)

    LOGGER.info("Write Excel data ...")
    write_freqs_to_excel(df_study1, "study1-output.xlsx")
    write_freqs_to_excel(df_study2, "study2-output.xlsx")

    LOGGER.info("Generate figures ...")
    generate_freqs_figures(df_study1, "figures_study1")
    generate_freqs_figures(df_study2, "figures_study2")

    # --------------------------------------------------

    LOGGER.info("Compute word importance ...")
    train_and_write_coefs_to_excel(df_study1, "study1-coefs.xlsx")
    train_and_write_coefs_to_excel(df_study2, "study2-coefs.xlsx")
    train_and_write_coefs_to_excel(df_study1, "study1-coefs-lemma.xlsx", lemma=True)
    train_and_write_coefs_to_excel(df_study2, "study2-coefs-lemma.xlsx", lemma=True)

    # --------------------------------------------------

    # optionally reload without stopwords removed
    # LOGGER.info("Load data ...")
    # df_study1, df_study2 = load_cached_data(do_clean_stopwords=False)

    LOGGER.info("Compute half-split word token rank correlation ...")
    random_state = 42
    generate_token_rank_correlation_plot(
        df_study1, dn_output="figures_study1", N=None, random_state=random_state
    )
    generate_token_rank_correlation_plot(
        df_study2, dn_output="figures_study2", N=None, random_state=random_state
    )

    LOGGER.info("Write Excel correlation data ...")
    compute_and_write_category_word_correlation_to_excel(df_study1, "study1-corrs.xlsx")
    compute_and_write_category_word_correlation_to_excel(df_study2, "study2-corrs.xlsx")
    compute_and_write_category_word_correlation_to_excel(
        df_study1, "study1-corrs-tfidf.xlsx", tfidf=True
    )
    compute_and_write_category_word_correlation_to_excel(
        df_study2, "study2-corrs-tfidf.xlsx", tfidf=True
    )

    LOGGER.info("Done.")


# --------------------------------------------------------------------------
