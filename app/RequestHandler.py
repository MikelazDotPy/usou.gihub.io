from flask import Flask, flash, redirect, render_template, request, session, abort


def main_page_render():
    return render_template("gg.html")