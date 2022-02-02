import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from scipy.constants import golden
from sklearn.metrics import confusion_matrix
import matplotlib.image

CLASSES = (
    "Ad Reinhardt",
    "Alberto Magnelli",
    "Alfred Manessier",
    "Anthony Caro",
    "Antoine Pevsner",
    "Auguste Herbin",
    "Aurélie Nemours",
    "Berto Lardera",
    "Charles Lapicque",
    "Charmion Von Wiegand",
    "César Domela",
    "Ellsworth Kelly",
    "Emilio Vedova",
    "Fernand Léger",
    "František Kupka",
    "Franz Kline",
    "François Morellet",
    "Georges Mathieu",
    "Georges Vantongerloo",
    "Gustave Singier",
    "Hans Hartung",
    "Jean Arp",
    "Jean Bazaine",
    "Jean Degottex",
    "Jean Dubuffet",
    "Jean Fautrier",
    "Jean Gorin",
    "Joan Mitchell",
    "Josef Albers",
    "Kenneth Noland",
    "Leon Polk Smith",
    "Lucio Fontana",
    "László Moholy-Nagy",
    "Léon Gischia",
    "Maria Helena Vieira da Silva",
    "Mark Rothko",
    "Morris Louis",
    "Naum Gabo",
    "Olle Bærtling",
    "Otto Freundlich",
    "Pierre Soulages",
    "Pierre Tal Coat",
    "Piet Mondrian",
    "Richard Paul Lohse",
    "Roger Bissière",
    "Sam Francis",
    "Sonia and Robert Delaunay",
    "Sophie Taeuber-Arp",
    "Theo van Doesburg",
    "Vassily Kandinsky",
    "Victor Vasarely",
    "Yves Klein",
    "Étienne Béothy",
)


def plot_accuracies(res, half_page_width):
    train_error = np.array(res[0])
    validation_error = np.array(res[1])
    test_error = res[2]

    fig = plt.figure(figsize=(half_page_width, half_page_width / golden))
    ax = fig.add_axes([0.15, 0.17, 0.8, 0.78])
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_ticks_position("left")
    ax.set_xlabel("Number of epochs")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 101)
    ax.grid(lw=0.5, zorder=-2, color="0.85", axis="y")
    ax.plot(100.0 - train_error, label="Training", lw=1.5)
    ax.plot(100.0 - validation_error, label="Validation", lw=1.5)
    ax.plot(
        len(validation_error) + 1,
        100.0 - test_error,
        ls="",
        marker="o",
        label="Test",
        color="C5",
    )
    ax.axhline(
        100 * 377.0 / 11503, ls="--", color="0.6", zorder=-1, label="Naive", lw=1.0
    )
    ax.legend(fontsize="smaller")
    fig.savefig("accuracies.pdf", dpi=300)


def plot_intra_class_variability(res, half_page_width, sample_folder):
    y_true, y_pred = np.array(res[4]), np.array(res[5])
    accuracies = np.empty(53)
    for i in range(53):
        accuracies[i] = 100.0 * sum((y_true == i) & (y_pred == i)) / sum(y_true == i)

    worst_idx = np.argmin(accuracies)
    best_idx = np.argmax(accuracies)
    print(f"most difficult artist: {CLASSES[worst_idx]}")
    print(f"easiest artist: {CLASSES[best_idx]}")
    hist, bins = np.histogram(accuracies, bins=10, range=(0.0, 100.0), density=False)

    samples_worst = [
        matplotlib.image.imread(
            os.path.join(sample_folder, CLASSES[worst_idx], f"{i}.jpg")
        )
        for i in range(3)
    ]
    samples_best = [
        matplotlib.image.imread(
            os.path.join(sample_folder, CLASSES[best_idx], f"{i}.jpg")
        )
        for i in range(3)
    ]

    fig = plt.figure(figsize=(2 * half_page_width, 1.1 * half_page_width / golden))

    ax_hist = fig.add_axes([0.1, 0.17, 0.4, 0.7])
    ax_hist.spines.right.set_visible(False)
    ax_hist.spines.top.set_visible(False)
    ax_hist.xaxis.set_ticks_position("bottom")
    ax_hist.yaxis.set_ticks_position("left")
    ax_hist.bar(bins[:-1] + 4.5, hist, width=9.0)
    ax_hist.set_xlabel("Accuracy (%)")
    ax_hist.set_ylabel("Count")
    ax_hist.set_xlim(0, 100)
    ax_hist.set_yticks(range(0, 14, 2))
    ax_hist.text(accuracies[worst_idx] - 2.0, 13.0, CLASSES[worst_idx])
    ax_hist.arrow(
        accuracies[worst_idx],
        12.8,
        0.0,
        -0.7,
        lw=0.7,
        width=0.05,
        head_width=0.8,
        head_length=0.2,
    )
    ax_hist.text(accuracies[best_idx] - 25.0, 13.0, CLASSES[best_idx])
    ax_hist.arrow(
        accuracies[best_idx],
        12.8,
        0.0,
        -0.7,
        lw=0.7,
        width=0.05,
        head_width=0.8,
        head_length=0.2,
    )

    ax_artists_names = fig.add_axes([0.6, 0.0, 0.34, 1.0], frameon=False)
    ax_artists_names.set_xticks([])
    ax_artists_names.set_yticks([])
    ax_artists_names.set_xlim(0.0, 1.0)
    ax_artists_names.set_ylim(0.0, 1.0)
    ax_artists_names.text(0.5, 0.925, CLASSES[worst_idx], horizontalalignment="center")
    ax_artists_names.text(0.5, 0.45, CLASSES[best_idx], horizontalalignment="center")
    add_sample_plot(fig, [0.55, 0.55, 0.15, 0.35], samples_worst[0])
    add_sample_plot(fig, [0.70, 0.55, 0.15, 0.35], samples_worst[1])
    add_sample_plot(fig, [0.85, 0.55, 0.15, 0.35], samples_worst[2])
    add_sample_plot(fig, [0.55, 0.075, 0.15, 0.35], samples_best[0])
    add_sample_plot(fig, [0.70, 0.075, 0.15, 0.35], samples_best[1])
    add_sample_plot(fig, [0.85, 0.075, 0.15, 0.35], samples_best[2])

    fig.savefig("intra_class_variability.pdf", dpi=300)


def add_sample_plot(fig, loc, sample):
    ax = fig.add_axes(loc, frameon=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.imshow(sample)


def plot_inter_class_similarity(res, half_page_width, sample_folder):
    y_true, y_pred = np.array(res[4]), np.array(res[5])
    cfm = confusion_matrix(y_true, y_pred, normalize="all")
    cfm = cfm - np.diag(cfm.diagonal())
    artist_0_idx, artist_1_idx = np.unravel_index(cfm.argmax(), cfm.shape)
    print(
        f"most confusing artists pair: {CLASSES[artist_0_idx]} & {CLASSES[artist_1_idx]}"
    )

    samples_0 = [
        matplotlib.image.imread(
            os.path.join(sample_folder, CLASSES[artist_0_idx], f"{i}.jpg")
        )
        for i in range(3)
    ]
    samples_1 = [
        matplotlib.image.imread(
            os.path.join(sample_folder, CLASSES[artist_1_idx], f"{i}.jpg")
        )
        for i in range(3)
    ]

    fig = plt.figure(figsize=(2 * half_page_width, 1.5 * half_page_width / golden))

    ax_cfm = fig.add_axes([0.05, 0.1, 0.4, 0.8], frameon=False)
    ax_cfm.text(
        26, -2, "Confusion matrix (without diagonal)", horizontalalignment="center"
    )
    ax_cfm.set_xticks([artist_1_idx])
    ax_cfm.set_yticks([artist_0_idx])
    ax_cfm.set_xticklabels([])
    ax_cfm.set_yticklabels([])
    ax_cfm.xaxis.set_tick_params(size=5.0, width=1.5)
    ax_cfm.yaxis.set_tick_params(size=5.0, width=1.5)
    ax_cfm.text(-5.0, artist_0_idx + 8, f"{CLASSES[artist_0_idx]}", rotation=90)
    ax_cfm.text(artist_1_idx - 3, 58, f"{CLASSES[artist_1_idx]}")
    cax = ax_cfm.imshow(cfm, cmap="inferno")
    cbar = plt.colorbar(cax, fraction=0.046, pad=0.03, extend="max")
    cbar.set_ticks([])
    cbar.set_label("Degree of confusion", fontsize="small")

    ax_artists_names = fig.add_axes([0.5, 0.0, 0.45, 1.0], frameon=False)
    ax_artists_names.set_xticks([])
    ax_artists_names.set_yticks([])
    ax_artists_names.set_xlim(0.0, 1.0)
    ax_artists_names.set_ylim(0.0, 1.0)
    ax_artists_names.text(
        0.5, 0.925, CLASSES[artist_0_idx], horizontalalignment="center"
    )
    ax_artists_names.text(
        0.5, 0.45, CLASSES[artist_1_idx], horizontalalignment="center"
    )
    add_sample_plot(fig, [0.5, 0.55, 0.15, 0.35], samples_0[0])
    add_sample_plot(fig, [0.65, 0.55, 0.15, 0.35], samples_0[1])
    add_sample_plot(fig, [0.8, 0.55, 0.15, 0.35], samples_0[2])
    add_sample_plot(fig, [0.5, 0.075, 0.15, 0.35], samples_1[0])
    add_sample_plot(fig, [0.65, 0.075, 0.15, 0.35], samples_1[1])
    add_sample_plot(fig, [0.8, 0.075, 0.15, 0.35], samples_1[2])

    fig.savefig("inter_class_similarity.pdf", dpi=300)


def main():
    half_page_width = 4.0
    results_filename = "../data/results.pkl"
    sample_folder = "../data/dataset/"

    with open(results_filename, "rb") as f:
        res = pickle.load(f)
    plot_accuracies(res, half_page_width)
    plot_intra_class_variability(res, half_page_width, sample_folder)
    plot_inter_class_similarity(res, half_page_width, sample_folder)


main()
